#include <stdio.h>
#include <string.h>
#include <algorithm>
using namespace std;
const int maxn = 20010;

int a[maxn], dp[maxn];
int V, n;

int main(){
	while(scanf("%d", &V) != EOF){
		scanf("%d", &n);
		for(int i = 1; i <= n; i++){
			scanf("%d", &a[i]);
		}
		memset(dp, 0, sizeof(dp));
		for(int i = 1; i <= n; i++){
			for(int v = V; v >= a[i]; v--){
				dp[v] = max(dp[v], dp[v - a[i]] + a[i]);
			}
		}
		int MAX = 0;
		for(int i = 0; i <= V; i++){
			if(dp[i] > MAX){
				MAX = dp[i];
			}
		}
		printf("%d\n", V - MAX);
	}
	return 0;
}