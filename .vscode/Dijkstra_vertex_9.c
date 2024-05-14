#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#define V 9  // 顶点数

// 定义一个结构体表示优先队列中的节点
typedef struct {
    int vertex;
    int dist;
} MinHeapNode;

// 定义一个结构体表示优先队列
typedef struct {
    int size;
    int capacity;
    int *pos;
    MinHeapNode **array;
} MinHeap;

// 创建一个新的优先队列节点
MinHeapNode* newMinHeapNode(int v, int dist) {
    MinHeapNode* minHeapNode = (MinHeapNode*)malloc(sizeof(MinHeapNode));
    minHeapNode->vertex = v;
    minHeapNode->dist = dist;
    return minHeapNode;
}

// 创建一个新的优先队列
MinHeap* createMinHeap(int capacity) {
    MinHeap* minHeap = (MinHeap*)malloc(sizeof(MinHeap));
    minHeap->pos = (int *)malloc(capacity * sizeof(int));
    minHeap->size = 0;
    minHeap->capacity = capacity;
    minHeap->array = (MinHeapNode**)malloc(capacity * sizeof(MinHeapNode*));
    return minHeap;
}

// 交换两个优先队列节点的位置
void swapMinHeapNode(MinHeapNode** a, MinHeapNode** b) {
    MinHeapNode* t = *a;
    *a = *b;
    *b = t;
}

// 堆化操作，维护优先队列的最小堆性质
void minHeapify(MinHeap* minHeap, int idx) {
    int smallest, left, right;
    smallest = idx;
    left = 2 * idx + 1;
    right = 2 * idx + 2;

    if (left < minHeap->size && minHeap->array[left]->dist < minHeap->array[smallest]->dist)
        smallest = left;

    if (right < minHeap->size && minHeap->array[right]->dist < minHeap->array[smallest]->dist)
        smallest = right;

    if (smallest != idx) {
        // 节点交换
        MinHeapNode *smallestNode = minHeap->array[smallest];
        MinHeapNode *idxNode = minHeap->array[idx];

        // 更新节点在堆中的位置
        minHeap->pos[smallestNode->vertex] = idx;
        minHeap->pos[idxNode->vertex] = smallest;

        // 节点交换
        swapMinHeapNode(&minHeap->array[smallest], &minHeap->array[idx]);

        minHeapify(minHeap, smallest);
    }
}

// 检查优先队列是否为空
int isEmpty(MinHeap* minHeap) {
    return minHeap->size == 0;
}

// 从优先队列中提取最小距离的顶点
MinHeapNode* extractMin(MinHeap* minHeap) {
    if (isEmpty(minHeap))
        return NULL;

    MinHeapNode* root = minHeap->array[0];

    MinHeapNode* lastNode = minHeap->array[minHeap->size - 1];
    minHeap->array[0] = lastNode;

    minHeap->pos[root->vertex] = minHeap->size - 1;
    minHeap->pos[lastNode->vertex] = 0;

    --minHeap->size;
    minHeapify(minHeap, 0);

    return root;
}

// 减少一个顶点的距离值，并调整优先队列的结构
void decreaseKey(MinHeap* minHeap, int v, int dist) {
    int i = minHeap->pos[v];
    minHeap->array[i]->dist = dist;

    while (i && minHeap->array[i]->dist < minHeap->array[(i - 1) / 2]->dist) {
        minHeap->pos[minHeap->array[i]->vertex] = (i-1)/2;
        minHeap->pos[minHeap->array[(i-1)/2]->vertex] = i;
        swapMinHeapNode(&minHeap->array[i], &minHeap->array[(i - 1) / 2]);

        i = (i - 1) / 2;
    }
}

// 检查一个顶点是否在优先队列中
int isInMinHeap(MinHeap *minHeap, int v) {
    if (minHeap->pos[v] < minHeap->size)
        return 1;
    return 0;
}

// 打印从源点到所有顶点的最短距离
void printArr(int dist[], int n) {
    printf("Vertex   Distance from Source\n");
    for (int i = 0; i < n; ++i)
        printf("%d \t\t %d\n", i, dist[i]);
}

// 打印从源点到某个顶点的路径
void printPath(int parent[], int j) {
    if (parent[j] == -1)
        return;

    printPath(parent, parent[j]);
    printf("%d ", j);
}

// 打印从源点到所有顶点的路径
void printSolution(int dist[], int n, int parent[]) {
    int src = 0;
    printf("Vertex\t Distance\tPath");
    for (int i = 1; i < V; i++) {
        printf("\n%d -> %d \t\t %d\t\t%d ", src, i, dist[i], src);
        printPath(parent, i);
    }
}

// Dijkstra算法
void dijkstra(int graph[V][V], int src) {
    int dist[V];
    int parent[V];
    int sptSet[V]; // sptSet[i]为1表示顶点i已在最短路径树中
    MinHeap* minHeap = createMinHeap(V);

    for (int v = 0; v < V; ++v) {
        dist[v] = INT_MAX;
        minHeap->array[v] = newMinHeapNode(v, dist[v]);
        minHeap->pos[v] = v;
        parent[v] = -1; // 初始化前驱节点
        sptSet[v] = 0;  // 初始化sptSet
    }

    minHeap->array[src] = newMinHeapNode(src, dist[src]);
    minHeap->pos[src] = src;
    dist[src] = 0;
    decreaseKey(minHeap, src, dist[src]);

    minHeap->size = V;

    while (!isEmpty(minHeap)) {
        MinHeapNode* minHeapNode = extractMin(minHeap);
        int u = minHeapNode->vertex;
        sptSet[u] = 1; // 标记顶点u为已处理

        for (int v = 0; v < V; ++v) {
            if (!sptSet[v] && graph[u][v] && dist[u] != INT_MAX && dist[u] + graph[u][v] < dist[v]) {
                dist[v] = dist[u] + graph[u][v];
                parent[v] = u; // 更新前驱节点
                decreaseKey(minHeap, v, dist[v]);
            }
        }
    }

    printSolution(dist, V, parent);
}

int main() {
    int graph[V][V] = { 
        {0, 4, 0, 0, 0, 0, 0, 8, 0},
        {4, 0, 8, 0, 0, 0, 0, 11, 0},
        {0, 8, 0, 7, 0, 4, 0, 0, 2},
        {0, 0, 7, 0, 9, 14, 0, 0, 0},
        {0, 0, 0, 9, 0, 10, 0, 0, 0},
        {0, 0, 4, 14, 10, 0, 2, 0, 0},
        {0, 0, 0, 0, 0, 2, 0, 1, 6},
        {8, 11, 0, 0, 0, 0, 1, 0, 7},
        {0, 0, 2, 0, 0, 0, 6, 7, 0}
    };

    dijkstra(graph, 0);

    return 0;
}
