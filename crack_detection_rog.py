#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
路面裂缝检测一键脚本（为 ROG 本地路径定制版本）

说明：
- 直接双击运行，或在命令行中运行：
    python crack_detection_rog.py
- 会自动：
    1）扫描 IMAGE_DIR 中的所有图片（目前写死为 1.jpg / 2.png / 064.jpg / 110.jpg / 317.jpg / 320.jpg）
    2）对每张图执行：预处理 → 分割 → 特征提取 → 参数测量
    3）在 OUTPUT_DIR 中生成：
        - overlay_*.jpg：叠加结果（红色轮廓 + 绿色骨架）
        - steps\每张图名\stepXX_*.png：中间处理步骤图
        - results.csv：每张图的长度、宽度、面积等数值
"""

import os
import math

import cv2
import numpy as np
import pandas as pd


# ===================== 需要你根据情况修改的路径部分 =====================

# 图片所在文件夹（你的当前路径）
IMAGE_DIR = r"C:\Users\ROG\Desktop\crack\image"

# 输出结果文件夹
OUTPUT_DIR = r"C:\Users\ROG\Desktop\crack\results"

# 要处理的图片文件名列表（就在 IMAGE_DIR 下面）
IMAGE_FILES = [
    "1.jpg",
    "2.png",
    "064.jpg",
    "110.jpg",
    "317.jpg",
    "320.jpg",
]

# 从图像顶部裁剪掉的比例：去人行道可以改成 0.3、0.4 等
CROP_TOP_RATIO = 0.0  # 先不裁剪，有需要你自己改成 0.4 之类即可


# 是否保存中间步骤图片
SAVE_STEPS = True

# ======================================================================

def hessian_frangi_like(gray: np.ndarray, sigmas=(1.0, 2.0, 3.0)) -> np.ndarray:
    """使用 Hessian 矩阵 + Frangi 思路做多尺度线结构增强（适合细长暗裂缝）。"""
    gray_f = gray.astype(np.float32)
    h, w = gray.shape
    vessel_all = np.zeros((h, w), dtype=np.float32)

    beta = 0.5  # 控制横向比率
    c = 15.0  # 控制强度响应

    for sigma in sigmas:
        blur = cv2.GaussianBlur(gray_f, (0, 0), sigmaX=sigma, sigmaY=sigma)
        Ixx = cv2.Sobel(blur, cv2.CV_32F, 2, 0, ksize=3)
        Iyy = cv2.Sobel(blur, cv2.CV_32F, 0, 2, ksize=3)
        Ixy = cv2.Sobel(blur, cv2.CV_32F, 1, 1, ksize=3)

        tmp = np.sqrt((Ixx - Iyy) ** 2 + 4.0 * Ixy * Ixy)
        l1 = 0.5 * (Ixx + Iyy + tmp)
        l2 = 0.5 * (Ixx + Iyy - tmp)

        abs_l1 = np.abs(l1)
        abs_l2 = np.abs(l2)
        swap_mask = abs_l1 < abs_l2

        l1_new = l1.copy()
        l2_new = l2.copy()
        l1_new[swap_mask] = l2[swap_mask]
        l2_new[swap_mask] = l1[swap_mask]

        l1 = l1_new
        l2 = l2_new

        eps = 1e-6
        Rb = (l2 / (l1 + eps)) ** 2
        S2 = l1 ** 2 + l2 ** 2

        cond = (l1 < 0)

        V = np.zeros_like(l1, dtype=np.float32)
        V[cond] = np.exp(-Rb[cond] / (2 * beta ** 2)) * (1.0 - np.exp(-S2[cond] / (2 * c ** 2)))

        vessel_all = np.maximum(vessel_all, V)

    vessel_norm = cv2.normalize(vessel_all, None, 0, 255, cv2.NORM_MINMAX)
    return vessel_norm.astype(np.uint8)


def morphological_skeleton(binary: np.ndarray) -> np.ndarray:
    """形态学骨架提取（迭代腐蚀 + 开运算差分）。"""
    img = (binary > 0).astype(np.uint8) * 255
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    skel = np.zeros_like(img)

    while True:
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()
        if cv2.countNonZero(img) == 0:
            break

    return skel


def compute_skeleton_length(skel: np.ndarray) -> float:
    """根据骨架图估计裂缝长度（像素）。"""
    coords = np.column_stack(np.where(skel > 0))
    if coords.size == 0:
        return 0.0

    skel_set = set(map(tuple, coords))
    length = 0.0

    for x, y in skel_set:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if (nx, ny) in skel_set:
                    if (x < nx) or (x == nx and y < ny):
                        if abs(dx) == 1 and abs(dy) == 1:
                            length += math.sqrt(2)
                        else:
                            length += 1.0
    return length


def filter_thin_components(binary: np.ndarray, min_area: int = 30, max_fill_ratio: float = 0.45) -> np.ndarray:
    """仅保留狭长裂缝连通域，过滤掉块状阴影或补丁。

    max_fill_ratio 控制 "面积 / 外接矩形面积"，越小说明越瘦长。
    """
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
    kept = np.zeros_like(binary)
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area < min_area:
            continue
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        fill_ratio = area / float(w * h + 1e-6)
        if fill_ratio <= max_fill_ratio:
            kept[labels == i] = 255
    return kept


def process_image(
    image_path: str,
    output_dir: str,
    crop_top_ratio: float = 0.0,
    save_steps: bool = False,
) -> dict:
    """处理单张图像：包含预处理、分割、骨架提取、参数测量，并可选保存中间步骤图。"""
    base_name = os.path.basename(image_path)
    name_no_ext, _ = os.path.splitext(base_name)

    steps_dir = None
    if save_steps:
        steps_dir = os.path.join(output_dir, "steps", name_no_ext)
        os.makedirs(steps_dir, exist_ok=True)

    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"无法读取图像：{image_path}")
    h, w, _ = img.shape

    crop_pixels = int(crop_top_ratio * h)
    if crop_pixels > 0:
        img_proc = img[crop_pixels:, :]
    else:
        img_proc = img.copy()
    if save_steps:
        cv2.imwrite(os.path.join(steps_dir, "step01_input_cropped.png"), img_proc)

    gray = cv2.cvtColor(img_proc, cv2.COLOR_BGR2GRAY)
    if save_steps:
        cv2.imwrite(os.path.join(steps_dir, "step02_gray.png"), gray)

    gray_blur = cv2.medianBlur(gray, 5)
    if save_steps:
        cv2.imwrite(os.path.join(steps_dir, "step03_gray_blur.png"), gray_blur)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray_clahe = clahe.apply(gray_blur)
    if save_steps:
        cv2.imwrite(os.path.join(steps_dir, "step04_gray_clahe.png"), gray_clahe)

    kernel_size = 21
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    background = cv2.morphologyEx(gray_clahe, cv2.MORPH_CLOSE, kernel)
    if save_steps:
        cv2.imwrite(os.path.join(steps_dir, "step05_background.png"), background)

    blackhat = cv2.subtract(background, gray_clahe)
    if save_steps:
        cv2.imwrite(os.path.join(steps_dir, "step06_blackhat.png"), blackhat)

    # === 改进：Frangi 线状增强（专门抓细裂缝），并与 blackhat 融合 ===
    frangi_resp = hessian_frangi_like(blackhat, sigmas=(0.8, 1.2, 1.6, 2.0))
    fused_resp = cv2.addWeighted(blackhat, 0.4, frangi_resp, 0.6, 0)
    fused_resp = cv2.GaussianBlur(fused_resp, (3, 3), 0)
    if save_steps:
        cv2.imwrite(os.path.join(steps_dir, "step06b_frangi.png"), frangi_resp)
        cv2.imwrite(os.path.join(steps_dir, "step06c_fused.png"), fused_resp)

    # === 改进阈值策略：融合图的百分位 + Otsu，偏向保留细线 ===
    non_zero_vals = fused_resp[fused_resp > 0]
    if non_zero_vals.size > 0:
        percentile_val = float(np.percentile(non_zero_vals, 80))
        otsu_val, _ = cv2.threshold(fused_resp, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        threshold_val = 0.55 * percentile_val + 0.45 * otsu_val
    else:
        percentile_val = None
        otsu_val, _ = cv2.threshold(fused_resp, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        threshold_val = otsu_val

    _, binary_thresh = cv2.threshold(fused_resp, threshold_val, 255, cv2.THRESH_BINARY)
    if save_steps:
        cv2.imwrite(os.path.join(steps_dir, "step07_binary_thresh.png"), binary_thresh)

    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    binary_clean = cv2.morphologyEx(binary_thresh, cv2.MORPH_OPEN, kernel_open)
    if save_steps:
        cv2.imwrite(os.path.join(steps_dir, "step08_binary_clean.png"), binary_clean)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary_clean, connectivity=8)
    min_area = 30
    filtered = np.zeros_like(binary_clean)
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            filtered[labels == i] = 255
    if save_steps:
        cv2.imwrite(os.path.join(steps_dir, "step09_filtered_area.png"), filtered)

    # === 改进：强制狭长约束，只保留细裂缝 ===
    thin_filtered = filter_thin_components(filtered, min_area=30, max_fill_ratio=0.45)
    if save_steps:
        cv2.imwrite(os.path.join(steps_dir, "step09b_filtered_thin.png"), thin_filtered)

    dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated_all = cv2.dilate(thin_filtered, dilate_kernel, iterations=1)
    if save_steps:
        cv2.imwrite(os.path.join(steps_dir, "step10_dilated.png"), dilated_all)

    num_labels_d, labels_d, stats_d, _ = cv2.connectedComponentsWithStats(dilated_all, connectivity=8)
    if num_labels_d > 1:
        areas = stats_d[1:, cv2.CC_STAT_AREA]
        max_idx = int(np.argmax(areas)) + 1
        dilated = np.zeros_like(dilated_all)
        dilated[labels_d == max_idx] = 255
    else:
        dilated = dilated_all

    skeleton_img = morphological_skeleton(dilated)
    skel_vis = (skeleton_img > 0).astype(np.uint8) * 255
    if save_steps:
        cv2.imwrite(os.path.join(steps_dir, "step11_skeleton.png"), skel_vis)

    area_pixels = int(np.sum(dilated > 0))
    length_pixels = compute_skeleton_length(skeleton_img)

    dist_transform = cv2.distanceTransform(dilated, cv2.DIST_L2, 5)
    skel_coords = np.column_stack(np.where(skeleton_img > 0))
    if skel_coords.size == 0:
        avg_width = 0.0
        max_width = 0.0
    else:
        local_widths = dist_transform[skel_coords[:, 0], skel_coords[:, 1]] * 2.0
        avg_width = float(np.mean(local_widths))
        max_width = float(np.max(local_widths))

    contours, _ = cv2.findContours(dilated.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    overlay = img_proc.copy()
    cv2.drawContours(overlay, contours, -1, (0, 0, 255), 2)
    for yx in skel_coords:
        cv2.circle(overlay, (int(yx[1]), int(yx[0])), 0, (0, 255, 0), 1)

    overlay_filename = f"overlay_{base_name}"
    overlay_path = os.path.join(output_dir, overlay_filename)
    if crop_pixels > 0:
        full_overlay = img.copy()
        full_overlay[crop_pixels:, :] = overlay
        cv2.imwrite(overlay_path, full_overlay)
    else:
        cv2.imwrite(overlay_path, overlay)

    if save_steps and steps_dir is not None:
        cv2.imwrite(os.path.join(steps_dir, "step12_overlay.png"), overlay)

    result = {
        "file": base_name,
        "crop_top_ratio": float(crop_top_ratio),
        "crop_pixels": int(crop_pixels),
        "threshold_val": float(threshold_val),
        "percentile_val": None if percentile_val is None else float(percentile_val),
        "otsu_val": None if otsu_val is None else float(otsu_val),
        "length_pixels": float(length_pixels),
        "avg_width_pixels": float(avg_width),
        "max_width_pixels": float(max_width),
        "area_pixels": int(area_pixels),
        "overlay_path": overlay_path,
    }
    return result


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    results = []
    for fname in IMAGE_FILES:
        img_path = os.path.join(IMAGE_DIR, fname)
        if not os.path.exists(img_path):
            print(f"[WARN] 找不到图像：{img_path}，跳过。")
            continue

        try:
            res = process_image(
                img_path,
                OUTPUT_DIR,
                crop_top_ratio=CROP_TOP_RATIO,
                save_steps=SAVE_STEPS,
            )
            results.append(res)
            print(
                f"[OK] {img_path}\n"
                f"     长度 = {res['length_pixels']:.2f} px, "
                f"平均宽度 = {res['avg_width_pixels']:.2f} px, "
                f"最大宽度 = {res['max_width_pixels']:.2f} px, "
                f"面积 = {res['area_pixels']} px², "
                f"阈值 = {res['threshold_val']:.2f} "
                f"(percentile={res['percentile_val']}, otsu={res['otsu_val']})\n"
                f"     叠加结果: {res['overlay_path']}"
            )
        except Exception as e:
            print(f"[ERROR] 处理 {img_path} 时出错: {e}")

    if results:
        csv_path = os.path.join(OUTPUT_DIR, "results.csv")
        df = pd.DataFrame(results)
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"[INFO] 所有结果已写入: {csv_path}")
    else:
        print("[INFO] 没有成功处理的图像。")


if __name__ == "__main__":
    main()
