#include <cstdio>
#include <algorithm>
#include <vector>
#include <queue>
#include <stack>
#include <cstring>
#include <map>

using std::queue;
using std::stack;
using std::vector;
using std::fill;
using std::map;

struct node
{
    int v;
    int w;
    node(int _v, int _w):v(_v), w(_w){}
};

const int MAXN = 20;
vector<node> G[MAXN];//图
int ve[MAXN], vl[MAXN];
int N;
stack<int> topOrder;
int inDegree[MAXN];
map<char, int> letterToIndex;//字母映射数字
vector<int> ans[MAXN];//关键路径
char str[MAXN];//输入的字母串

//拓扑排序
bool topologicalSort(){

    queue<int> q;
    for (int i = 0; i < N; ++i)
    {
        if(inDegree[i] == 0){
            q.push(i);
        }
    }

    while(!q.empty()){
        int u = q.front();
        q.pop();

        topOrder.push(u);
        for (int i = 0; i < G[u].size(); ++i)
        {
            int v = G[u][i].v;
            inDegree[v]--;
            if(inDegree[v] == 0){
                q.push(v);
            }
            if(ve[u] + G[u][i].w > ve[v]){
                ve[v] = ve[u] + G[u][i].w;
            }
        }
    }

    if(topOrder.size() == N) return true;
    else return false;
}


int CriticalPath(){
    memset(ve, 0, sizeof(ve));
    if(topologicalSort() == false){//求ve
        return -1;
    }
    int maxLength = 0;
    for (int i = 0; i < N; ++i)
    {
        if(ve[i] > maxLength){
            maxLength = ve[i];
        }
    }
    fill(vl, vl + MAXN, maxLength);

    while(!topOrder.empty()){//逆拓扑排序，求vl
        int u = topOrder.top();
        topOrder.pop();
        for (int i = 0; i < G[u].size(); ++i)
        {
            int v = G[u][i].v;
            if(vl[v] - G[u][i].w < vl[u]){
                vl[u] = vl[v] - G[u][i].w;
            }
        }
    }

    for (int i = 0; i < N; ++i)//清空上一次关键路径
    {
        ans[i].clear();
    }

    for (int u = 0; u < N; ++u)
    {
        for (int i = 0; i < G[u].size(); ++i)
        {
            int v = G[u][i].v, w = G[u][i].w;
            int e = ve[u], l = vl[v] - w;
            if(e == l){//是关键活动，则存入关键路径
                ans[u].push_back(v);
            }
        }
    }

    int s;
    for (int i = 0; i < N; ++i)//寻找事件起始点
    {
        if(ve[i] == 0){
            s = i;
            break;
        }
    }

    while(ans[s].size()){//没有后继结点时，退出
        printf("(%c,%c) ", str[s], str[ans[s][0]]);
        s = ans[s][0];
    }
    return ve[N - 1];//return maxLength;
}

int main(int argc, char const *argv[])
{
    int n, m, w;
    char a, b;
    scanf("%d", &n);
    for (int i = 0; i < n; ++i)
    {
        memset(inDegree, 0, sizeof(inDegree));

        scanf("%d%d", &N, &m);
        for (int j = 0; j < N; ++j)
        {
            G[j].clear();
        }

        scanf("%s", str);
        for (int j = 0; j < N; ++j)
        {
            letterToIndex[str[j]] = j;
        }

        for (int j = 0; j < m; ++j)
        {
            //getchar();
            scanf("%*c%c %c %d", &a, &b, &w);
            G[letterToIndex[a]].push_back(node(letterToIndex[b], w));
            inDegree[letterToIndex[b]]++;
        }

        int length = CriticalPath();
        printf("%d\n", length);
    }
    return 0;
}
