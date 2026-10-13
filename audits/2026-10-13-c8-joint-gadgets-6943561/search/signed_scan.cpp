// Boundary chords are Eq/Diff; all remaining edges retain Diff.
// Discovery scanner, independent output file from the pure-cap certificates.
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
int rows[274][8], upper[8][16][274];
vector<int> adj[13];
int colour[13], ord[13], n, h;
ofstream tuple_output;
unsigned int count_lifts(int depth) {
    if(depth==h){
        unsigned int encoded=0;for(int i=0;i<h;++i)encoded|=colour[8+i]<<(2*i);
        tuple_output.put(encoded&255);tuple_output.put(encoded>>8);return 1;
    }
    int v=ord[depth],forbidden=0;
    for(int w:adj[v])if(colour[w]>=0)forbidden|=1<<colour[w];
    unsigned int total=0;
    for(int c=0;c<4;++c)if(!(forbidden&(1<<c))){colour[v]=c;total+=count_lifts(depth+1);}
    colour[v]=-1;return total;
}
int findroot(int *parent,int a){while(parent[a]!=a)a=parent[a];return a;}
int main(int argc,char **argv){
    assert(argc==7);ifstream conf(argv[1]),graphs(argv[2]);ofstream out(argv[3]);
    ofstream count_output(argv[4],ios::binary),sign_output(argv[6],ios::binary);tuple_output.open(argv[5],ios::binary);
    assert(conf&&graphs&&out&&count_output&&tuple_output&&sign_output);
    for(auto&r:rows)for(int&c:r)conf>>c;
    for(auto&q:upper)for(auto&t:q)for(int&v:t)conf>>v;
    int index[65536];fill(index,index+65536,-1);
    for(int r=0;r<274;++r){int key=0;for(int i=0;i<8;++i)key|=rows[r][i]<<(2*i);index[key]=r;}
    int transformed_row[16][274];
    for(int t=0;t<16;++t)for(int r=0;r<274;++r){
        int d=t<8?1:-1,s=t%8,p[8],rename[4]={-1,-1,-1,-1},next=0,key=0;
        for(int j=0;j<8;++j)p[(s+d*j+8)%8]=rows[r][j];
        for(int j=0;j<8;++j){if(rename[p[j]]<0)rename[p[j]]=next++;key|=rename[p[j]]<<(2*j);}
        transformed_row[t][r]=index[key];assert(index[key]>=0);
    }
    uint64_t total=0,valid_signatures=0,rejections=0,full_lifts=0,empty_fibres=0;
    bool forced[8][274]={};
    int minima[8];fill(minima,minima+8,275);
    string line;
    while(getline(graphs,line)){
        istringstream is(line);string code;is>>n>>code;assert(n>=8&&n<=13);h=n-8;
        vector<vector<int>>rot(n);int v=0;
        for(char c:code){if(c==',')++v;else rot[v].push_back(c-'a');}assert(v==n-1);
        bool seen[13][13]={};vector<int>boundary;int face_count=0,edge_count=0;
        for(int a=0;a<n;++a)for(int b:rot[a]){
            ++edge_count;if(seen[a][b])continue;vector<int>face;int u=a,w=b;
            do{assert(!seen[u][w]);seen[u][w]=true;face.push_back(u);auto&r=rot[w];auto it=find(r.begin(),r.end(),u);assert(it!=r.end());int next=r[(it-r.begin()+1)%r.size()];u=w;w=next;}while(u!=a||w!=b);
            ++face_count;if(face.size()==8){assert(boundary.empty());boundary=face;}else assert(face.size()==3);
        }
        assert(boundary.size()==8&&n-edge_count/2+face_count==2);
        int named[13];fill(named,named+13,-1);for(int i=0;i<8;++i)named[boundary[i]]=i;
        int next=8;for(int i=0;i<n;++i)if(named[i]<0)named[i]=next++;
        for(auto&a:adj)a.clear();
        vector<pair<int,int>>chords;
        for(int i=0;i<n;++i)for(int j:rot[i]){
            int a=named[i],b=named[j];
            if(a<8&&b<8&&((a-b+8)%8!=1)&&((b-a+8)%8!=1)){
                if(a<b)chords.emplace_back(a,b);
            }else adj[a].push_back(b);
        }
        sort(chords.begin(),chords.end());int m=chords.size();assert(m<=5);
        bool valid[32]={};int saved[32]={};
        for(int mask=0;mask<(1<<m);++mask){
            int parent[8];for(int i=0;i<8;++i)parent[i]=i;
            for(int j=0;j<m;++j)if(mask>>j&1){auto[a,b]=chords[j];parent[findroot(parent,a)]=findroot(parent,b);}
            bool ok=true;int blocks=0;
            for(int i=0;i<8;++i){ok&=findroot(parent,i)!=findroot(parent,(i+1)%8);blocks+=findroot(parent,i)==i;}
            for(int j=0;j<m;++j)if(!(mask>>j&1)){auto[a,b]=chords[j];ok&=findroot(parent,a)!=findroot(parent,b);}
            valid[mask]=ok;saved[mask]=8-blocks;valid_signatures+=ok;
        }
        for(int i=0;i<h;++i)ord[i]=8+i;
        sort(ord,ord+h,[](int a,int b){int da=0,db=0;for(int w:adj[a])da+=(w<8?20:1);for(int w:adj[b])db+=(w<8?20:1);return da!=db?da>db:a<b;});
        int counts[274],sign[274];
        for(int r=0;r<274;++r){
            fill(colour,colour+13,-1);copy(rows[r],rows[r]+8,colour);counts[r]=count_lifts(0);sign[r]=0;
            for(int j=0;j<m;++j){auto[a,b]=chords[j];if(colour[a]==colour[b])sign[r]|=1<<j;}
            assert(valid[sign[r]]);
            count_output.put(counts[r]&255);count_output.put(counts[r]>>8);sign_output.put(sign[r]);
            full_lifts+=counts[r];empty_fibres+=counts[r]==0;
        }
        for(int q=0;q<8;++q)for(int t=0;t<16;++t){
            int hit[32]={},last[32]={};for(int r=0;r<274;++r)if(counts[r]&&upper[q][t][r]){++hit[sign[r]];last[sign[r]]=r;}
            for(int mask=0;mask<(1<<m);++mask)if(valid[mask]){
                minima[q]=min(minima[q],hit[mask]);
                if(hit[mask]==1){
                    int row=transformed_row[t][last[mask]];
                    if(!forced[q][row]){
                        forced[q][row]=true;
                        out<<"{\"kind\":\"forced_row\",\"private_vertices\":"<<h<<",\"graph_index\":"<<total<<",\"query_index\":"<<q<<",\"transform\":"<<t<<",\"equality_mask\":"<<mask<<",\"forced_row\":"<<row<<",\"saved_boundary_vertices\":"<<saved[mask]<<",\"ascii\":\""<<line<<"\",\"chords\":[";
                        for(int j=0;j<m;++j){if(j)out<<',';out<<'['<<chords[j].first<<','<<chords[j].second<<']';}out<<"]}\n";
                    }
                }
                if(hit[mask]==0){
                    ++rejections;
                    out<<"{\"kind\":\"rejection\",\"private_vertices\":"<<h<<",\"graph_index\":"<<total<<",\"query_index\":"<<q<<",\"transform\":"<<t<<",\"equality_mask\":"<<mask<<",\"saved_boundary_vertices\":"<<saved[mask]<<",\"ascii\":\""<<line<<"\",\"chords\":[";
                    for(int j=0;j<m;++j){if(j)out<<',';out<<'['<<chords[j].first<<','<<chords[j].second<<']';}out<<"]}\n";out.flush();
                    if(rejections==1)cerr<<"FIRST REJECTION: h="<<h<<" graph="<<total<<" query="<<q<<" transform="<<t<<" mask="<<mask<<'\n';
                }
            }
        }
        ++total;
    }
    out<<"{\"kind\":\"summary\",\"graphs\":"<<total<<",\"valid_signed_graphs\":"<<valid_signatures<<",\"rejections\":"<<rejections<<",\"full_lifts_ignoring_chords\":"<<full_lifts<<",\"empty_fibres_ignoring_chords\":"<<empty_fibres<<",\"minimum_intersections\":[";
    for(int i=0;i<8;++i){if(i)out<<',';out<<minima[i];}out<<"],\"forced_rows\":[";
    for(int q=0;q<8;++q){if(q)out<<',';out<<'[';bool first=true;for(int r=0;r<274;++r)if(forced[q][r]){if(!first)out<<',';first=false;out<<r;}out<<']';}out<<"]}\n";
    cerr<<total<<" graphs; "<<valid_signatures<<" valid signatures; "<<rejections<<" rejecting graph-sign-query-orientations\n";
}
