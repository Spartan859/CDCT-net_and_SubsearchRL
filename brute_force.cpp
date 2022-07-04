#include<bits/stdc++.h>
#define rep(I,a,b) for(int I=(a);I<=(b);I++)
#define ll long long
using namespace std;
const int N=1e5+5,M=105,INF=1e9+5,s=100;
int n,m;
double dp[N][M];
double traj[N][3],q[N][3];
inline double dist(int a,int b){
    double rt=0;
    rep(i,0,2)
        rt+=(traj[a][i]-q[b][i])*(traj[a][i]-q[b][i]);
    return sqrt(rt);
}
void solve(){
    double ans=INF;int bl,br;
    rep(i,1,n){
        dp[i-1][1]=dp[i][1]=0;
        int ed=min(n,i+s-1);
        rep(j,i,ed){
            rep(k,1,m){
                if(k==1) dp[j][k]=dist(j,k)+dp[j-1][k];
                else if(j==i) dp[j][k]=dist(j,k)+dp[j][k-1];
                else dp[j][k]=
                dist(j,k)+min(min(dp[j-1][k],dp[j][k-1]),dp[j-1][k-1]);
            }
            if(dp[j][m]<ans){
                ans=dp[j][m];
                bl=i;br=j;
            }
        }
    }
    printf("%.4lf %d %d\n",ans/10,bl,br);
}
inline void input(){
    scanf("%d",&n);
    rep(i,1,n) scanf("%lf%lf%lf",&traj[i][0],&traj[i][1],&traj[i][2]);
    scanf("%d",&m);
    rep(i,1,m) scanf("%lf%lf%lf",&q[i][0],&q[i][1],&q[i][2]);
}
int main(){
    freopen("ans_ppo.txt","w",stdout);
    //cout<<"!!!";
    rep(i,1,500){
        // string tmp=;
        //cout<<"!!!";
        freopen(("seq2021_10_11_18_19_28/data/"+to_string(i)+".txt").c_str(),"r",stdin);
        cout<<endl;
        //cout<<"!!?";
        //fflush(stdin);
        input();
        solve();
        //fflush(stdin);
        //fclose(stdin);
    }
    return 0;
}