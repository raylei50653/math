/* Output-only filter. No generation-recursion pruning or automorphism assumptions.
 * Each sphere, every degree-five root, and all ten ordered boundary frames.
 * Compile with the frozen plantri.c and -DPLUGIN=filter.c; use -m5 -u.
 */
#include <stdint.h>
#define FILTER r6_filter
#define SUMMARY r6_summary
static unsigned long long tally[11];
static const char *labels[11] = {"spheres", "roots5", "frames_degree444",
  "induced_boundary", "unique_apices", "apex_degrees", "boundary_excess",
  "apex_skeleton", "r_fan", "seven_pin_edges", "emitted_spheres"};
static uint64_t adj6[MAXN];
static int rot6[MAXN][MAXN];
static int edge6(int a,int b) { return (adj6[a] >> b) & 1; }
static void list6(int *xs,int n) {
  int i; putchar('['); for(i=0;i<n;++i) printf("%s%d",i?",":"",xs[i]); putchar(']');
}
static int r6_filter(int nbtot,int nbop,int doflip) {
  int i,j,u,sg,start,B[5],A[5],C[7],v,w,r,s,t,p,q,x,y,a,b,c;
  int emitted=0,ok,ri,rsign; uint64_t bm,common,um[7];
  (void)nbtot;(void)nbop;(void)doflip;
  if(nv>63) { fprintf(stderr,"unsupported nv\n"); exit(2); }
  ++tally[0];
  for(i=0;i<nv;++i) {
    EDGE *e=firstedge[i]; adj6[i]=0;
    for(j=0;j<degree[i];++j,e=e->next) {
      rot6[i][j]=e->end; adj6[i] |= (uint64_t)1 << e->end;
    }
  }
  for(u=0;u<nv;++u) if(degree[u]==5) {
    ++tally[1];
    for(sg=-1;sg<=1;sg+=2) for(start=0;start<5;++start) {
      for(i=0;i<5;++i) B[i]=rot6[u][(start+sg*i+10)%5];
      x=B[0];y=B[1];a=B[2];b=B[3];c=B[4];
      if(degree[x]!=5 || degree[y]!=5 || degree[b]!=5) continue;
      ++tally[2]; ok=1;bm=0;
      for(i=0;i<5;++i) bm|=(uint64_t)1<<B[i];
      for(i=0;i<5;++i) for(j=i+1;j<5;++j)
        if(edge6(B[i],B[j]) != (j==i+1 || (i==0&&j==4))) ok=0;
      if(!ok) continue; ++tally[3];
      for(i=0;i<5;++i) {
        common=adj6[B[i]]&adj6[B[(i+1)%5]]&~(bm|((uint64_t)1<<u));
        if(__builtin_popcountll(common)!=1) {ok=0;break;}
        A[i]=__builtin_ctzll(common);
        if((adj6[A[i]]&bm)!=(((uint64_t)1<<B[i])|((uint64_t)1<<B[(i+1)%5]))) ok=0;
        for(j=0;j<i;++j) if(A[i]==A[j]) ok=0;
      }
      if(!ok)continue; ++tally[4];
      r=A[0];t=A[1];p=A[2];q=A[3];s=A[4];
      if(degree[r]!=6 || degree[s]<6 || degree[t]<6)continue;
      ++tally[5];
      if(degree[a]+degree[c]-10<3)continue;
      ++tally[6];
      if(!edge6(r,s)||!edge6(r,t)||!edge6(p,q)||edge6(r,p)||edge6(r,q)
        ||edge6(s,t)||edge6(s,p)||edge6(t,q)
        ||edge6(t,p)!=(degree[a]==5)||edge6(s,q)!=(degree[c]==5)
        ||(edge6(t,p)&&edge6(s,q)))continue;
      ++tally[7];
      ri=0;while(rot6[r][ri]!=x)++ri;
      rsign=rot6[r][(ri+1)%6]==y?1:-1;
      if(rot6[r][(ri+rsign+6)%6]!=y || rot6[r][(ri+2*rsign+12)%6]!=t
         ||rot6[r][(ri+5*rsign+30)%6]!=s)continue;
      w=rot6[r][(ri+3*rsign+18)%6];v=rot6[r][(ri+4*rsign+24)%6];
      if((bm>>v&1)||(bm>>w&1)||v==p||v==q||w==p||w==q)continue;
      ++tally[8];
      C[0]=a;C[1]=s;C[2]=v;C[3]=w;C[4]=t;C[5]=p;C[6]=q;
      for(i=0;i<7;++i) um[i]=0;
      for(i=0;i<7;++i)for(j=i+1;j<7;++j) {
        int e=i==0?(edge6(a,C[j])||edge6(c,C[j])):edge6(C[i],C[j]);
        int allowed=(i<5&&j<5&&(j==i+1||(i==0&&j==4)))
          ||(i==0&&j>=5)||(i==5&&j==6)||(i==4&&j==5)||(i==1&&j==6);
        int required=allowed && !(i==4&&j==5) && !(i==1&&j==6);
        if((required&&!e)||(!allowed&&e))ok=0;
      }
      if(!ok)continue; ++tally[9];
      if(!emitted) {
        printf("{\"sphere\":%llu,\"rotation\":[",tally[0]-1);
        for(i=0;i<nv;++i){if(i)putchar(',');list6(rot6[i],degree[i]);}
        printf("],\"frames\":[");emitted=1;++tally[10];
      } else putchar(',');
      printf("{\"root\":%d,\"B\":",u);list6(B,5);
      printf(",\"apices\":");list6(A,5);
      printf(",\"v\":%d,\"w\":%d}",v,w);
    }
  }
  if(emitted)printf("]}\n");
  return 0;
}
static void r6_summary(void) {
  int i;fprintf(msgfile,"R6_COUNTS {");
  for(i=0;i<11;++i)fprintf(msgfile,"%s\"%s\":%llu",i?",":"",labels[i],tally[i]);
  fprintf(msgfile,"}\n");
}
