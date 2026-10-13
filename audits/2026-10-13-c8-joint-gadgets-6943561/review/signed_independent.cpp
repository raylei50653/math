// Independent signed-cap replay: all private assignments, bitset compatibility,
// and transitive closure of Eq chords. Does not include producer source.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
using Bits=array<uint64_t,5>;
int main(int argc,char**argv){
 assert(argc==7);
 ifstream cfg(argv[1]),graphs(argv[2]),counts(argv[3],ios::binary),tuples(argv[4],ios::binary),signatures(argv[5],ios::binary);
 ofstream result(argv[6]);assert(cfg&&graphs&&counts&&tuples&&signatures&&result);
 array<array<int,8>,274>rows;for(auto&r:rows)for(int&x:r)cfg>>x;
 Bits allowed[8][16]{};for(int v=0;v<8;v++)for(int f=0;f<16;f++)for(int r=0;r<274;r++)
  if(!(f&(1<<rows[r][v])))allowed[v][f][r/64]|=uint64_t(1)<<(r%64);
 int trans[16][274];for(auto&t:trans)for(int&x:t)cfg>>x;
 int accept[8][274];for(auto&q:accept)for(int&x:q)cfg>>x;assert(cfg);
 Bits accepted[8][16]{};for(int q=0;q<8;q++)for(int t=0;t<16;t++)for(int r=0;r<274;r++)
  if(accept[q][trans[t][r]])accepted[q][t][r/64]|=uint64_t(1)<<(r%64);
 uint64_t graphnum=0,validnum=0,empty=0,lifts=0,tests=0,rejections=0;
 int minima[8];fill(minima,minima+8,275);bool forced[8][274]{};
 vector<array<int,5>>cache[6][1024];bool cached[6][1024]{};
 string line;
 while(getline(graphs,line)){
  istringstream ss(line);int n;string code;ss>>n>>code;assert(n>=8&&n<=13);
  vector<vector<int>>rot(n);int v=0;for(char c:code){if(c==',')v++;else rot[v].push_back(c-'a');}assert(v==n-1);
  bool edge[13][13]{};int E=0;
  for(int i=0;i<n;i++)for(int j:rot[i]){assert(j>=0&&j<n&&j!=i&&!edge[i][j]);edge[i][j]=true;E++;}
  for(int i=0;i<n;i++)for(int j=0;j<n;j++)assert(edge[i][j]==edge[j][i]);
  bool seen[13][13]{};vector<int>B;int F=0;
  for(int i=0;i<n;i++)for(int j:rot[i])if(!seen[i][j]){
   vector<int>face;int a=i,b=j;
   do{assert(!seen[a][b]);seen[a][b]=true;face.push_back(a);auto at=find(rot[b].begin(),rot[b].end(),a);assert(at!=rot[b].end());int c=rot[b][(at-rot[b].begin()+1)%rot[b].size()];a=b;b=c;}while(a!=i||b!=j);
   F++;if(face.size()==8){assert(B.empty());B=face;}else assert(face.size()==3);
  }
  assert(n-E/2+F==2&&E/2==3*n-11&&B.size()==8);
  auto uniq=B;sort(uniq.begin(),uniq.end());assert(unique(uniq.begin(),uniq.end())==uniq.end());
  vector<int>I;for(int i=0;i<n;i++)if(find(B.begin(),B.end(),i)==B.end())I.push_back(i);
  vector<pair<int,int>>chords;for(int i=0;i<8;i++)for(int j=i+1;j<8;j++)if(j!=i+1&&!(i==0&&j==7)&&edge[B[i]][B[j]])chords.emplace_back(i,j);
  assert(chords.size()<=5);bool valid[32]{};int ns=1<<chords.size(),ngood=0;
  for(int sign=0;sign<ns;sign++){
   bool eq[8][8]{};for(int i=0;i<8;i++)eq[i][i]=true;
   for(unsigned int j=0;j<chords.size();j++)if(sign>>j&1){auto[a,b]=chords[j];eq[a][b]=eq[b][a]=true;}
   for(int k=0;k<8;k++)for(int i=0;i<8;i++)for(int j=0;j<8;j++)eq[i][j]=eq[i][j]||(eq[i][k]&&eq[k][j]);
   bool ok=true;for(int i=0;i<8;i++)if(eq[i][(i+1)%8])ok=false;
   for(unsigned int j=0;j<chords.size();j++)if(!(sign>>j&1)){auto[a,b]=chords[j];if(eq[a][b])ok=false;}
   valid[sign]=ok;ngood+=ok;
  }
  int h=I.size(),key=0,z=0;vector<pair<int,int>>pe;
  for(int i=0;i<h;i++)for(int j=i+1;j<h;j++,z++)if(edge[I[i]][I[j]]){key|=1<<z;pe.emplace_back(i,j);}
  if(!cached[h][key]){
   for(int word=0;word<(1<<(2*h));word++){array<int,5>p{};for(int i=0;i<h;i++)p[i]=(word>>(2*i))&3;bool ok=true;for(auto[a,b]:pe)if(p[a]==p[b])ok=false;if(ok)cache[h][key].push_back(p);}cached[h][key]=true;
  }
  int expected[274]{};vector<int>expected_tuples[274];
  for(const auto&p:cache[h][key]){
   int word=0;for(int j=0;j<h;j++)word|=p[j]<<(2*j);
   Bits b;for(int k=0;k<5;k++)b[k]=~uint64_t(0);b[4]=(uint64_t(1)<<18)-1;
   for(int i=0;i<8;i++){int mask=0;for(int j=0;j<h;j++)if(edge[B[i]][I[j]])mask|=1<<p[j];for(int k=0;k<5;k++)b[k]&=allowed[i][mask][k];}
   for(int k=0;k<5;k++)while(b[k]){int bit=__builtin_ctzll(b[k]);int row=k*64+bit;expected[row]++;expected_tuples[row].push_back(word);b[k]&=b[k]-1;}
  }
  Bits support[32]{};int nonempty=0;
  for(int r=0;r<274;r++){
   int lo=counts.get(),hi=counts.get();assert(lo>=0&&hi>=0);
   if(lo+256*hi!=expected[r]){cerr<<"count mismatch graph "<<graphnum<<" row "<<r<<endl;return 2;}
   vector<int>got;for(int i=0;i<expected[r];i++){int a=tuples.get(),b=tuples.get();assert(a>=0&&b>=0);got.push_back(a+256*b);}sort(got.begin(),got.end());
   if(got!=expected_tuples[r]){cerr<<"tuple mismatch graph "<<graphnum<<" row "<<r<<endl;return 3;}
   int s=0;for(unsigned int j=0;j<chords.size();j++){auto[a,b]=chords[j];if(rows[r][a]==rows[r][b])s|=1<<j;}
   assert(valid[s]);int given=signatures.get();assert(given>=0);if(given!=s){cerr<<"signature mismatch graph "<<graphnum<<" row "<<r<<endl;return 4;}
   if(expected[r]){nonempty++;support[s][r/64]|=uint64_t(1)<<(r%64);}lifts+=expected[r];
  }
  validnum+=ngood;empty+=uint64_t(ngood)*274-nonempty;
  for(int s=0;s<ns;s++)if(valid[s])for(int q=0;q<8;q++)for(int t=0;t<16;t++){
   int hit=0,sole=-1;for(int k=0;k<5;k++){uint64_t b=support[s][k]&accepted[q][t][k];hit+=__builtin_popcountll(b);if(b)sole=k*64+__builtin_ctzll(b);}
   minima[q]=min(minima[q],hit);rejections+=hit==0;if(hit==1)forced[q][trans[t][sole]]=true;tests++;
  }
  graphnum++;
 }
 assert(counts.get()==EOF&&tuples.get()==EOF&&signatures.get()==EOF);
 result<<"{\"graphs\":"<<graphnum<<",\"valid_signed_graphs\":"<<validnum<<",\"signed_fibres\":"<<validnum*274<<",\"empty_signed_fibres\":"<<empty<<",\"full_lifts\":"<<lifts<<",\"cap_query_checks\":"<<tests<<",\"rejections\":"<<rejections<<",\"minimum_intersections\":[";
 for(int i=0;i<8;i++){if(i)result<<',';result<<minima[i];}result<<"],\"forced_rows\":[";
 for(int q=0;q<8;q++){if(q)result<<',';result<<'[';bool first=true;for(int r=0;r<274;r++)if(forced[q][r]){if(!first)result<<',';first=false;result<<r;}result<<']';}result<<"]}\n";
}
