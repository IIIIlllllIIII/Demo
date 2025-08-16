#include <stdio.h>

// 假设一个完全二叉树的节点个数为100（1-99），使用数组模拟
#define MAX_NODES 100

void printRightLeafToRoot(int tree[MAX_NODES]) {
    // 从最后一层开始，找到最右边的叶子节点
    for (int level = 1; (1 << level) <= MAX_NODES; level++) {
        // 最后一层的第一个节点索引
        int start = (1 << (level - 1));
        // 如果当前层是最后一层，直接打印最右侧节点
        if ((1 << level) > MAX_NODES) {
            printf("%d ", tree[MAX_NODES - 1]);
            continue;
        }
        // 遍历当前层，打印每个叶子节点
        for (int i = start + (1 << (level - 1)) - 2; i >= start; i--) {
            // 检查是否为叶子节点（假设叶子节点是那些没有孩子的节点）
            if (i * 2 > MAX_NODES || i * 2 + 1 > MAX_NODES) {
                printf("%d ", tree[i]);
            }
        }
    }
}

int main() {
    int tree[MAX_NODES]; // 假设tree已经被正确填充了1-99的数字，按照完全二叉树的规则排列
    // 为了简化，我们这里手动填充这个数组，正常情况下这个数组应该是由某种逻辑生成的
    for (int i = 0; i < MAX_NODES; i++) {
        tree[i] = i + 1;
    }
    
    printf("遍历结果（从右到左，从叶到根）:");
    printRightLeafToRoot(tree);
    return 0;
}