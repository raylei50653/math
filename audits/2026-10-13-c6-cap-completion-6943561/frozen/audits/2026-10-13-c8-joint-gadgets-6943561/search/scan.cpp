// Exact full C8 extension supports and counts for plantri disk rotations.
// Input config: 274 canonical rows, then 8*16 transformed support bit rows.
// Input graph file: plantri -aP8c2m2 n ASCII rotations, n in [8,13].
// Output binary: per graph 274 uint16 little-endian complete fibre counts.
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
    if (depth>=h) {
        unsigned int encoded=0;
        for(int i=0;i<h;++i) encoded|=colour[8+i]<<(2*i);
        tuple_output.put(encoded&255);tuple_output.put(encoded>>8);
        return 1;
    }
    int v=ord[depth], forbidden=0;
    for(int w:adj[v]) if(colour[w]>=0) forbidden|=1<<colour[w];
    unsigned int count=0;
    for(int c=0;c<4;++c) if(!(forbidden&(1<<c))) {
        colour[v]=c; count+=count_lifts(depth+1);
    }
    colour[v]=-1;
    return count;
}
int main(int argc,char** argv) {
    assert(argc==6);
    ifstream conf(argv[1]), graphs(argv[2]);
    ofstream out(argv[3],ios::binary), stats(argv[4]);
    tuple_output.open(argv[5],ios::binary);
    assert(conf&&graphs&&out&&stats&&tuple_output);
    for(auto &r:rows) for(int &c:r) conf>>c;
    for(auto &q:upper) for(auto &s:q) for(int &v:s) conf>>v;
    assert(conf);
    uint64_t total=0, empty=0, lifts=0, rejects[8]={};
    int minima[8]; uint64_t witness[8]={}; int witness_transform[8]={};
    fill(minima,minima+8,275);
    string line;
    while(getline(graphs,line)) {
        istringstream input(line);string encoded;input>>n>>encoded;
        assert(n>=8&&n<=13);h=n-8;
        vector<vector<int>> rotation(n);
        int v=0;
        for(char c:encoded) {
            if(c==',') ++v;
            else {assert(c>='a'&&c<'a'+n);rotation[v].push_back(c-'a');}
        }
        assert(v==n-1);
        bool seen[13][13]={};vector<int> boundary;
        int face_count=0, edge_count=0;
        for(int a=0;a<n;++a) for(int b:rotation[a]) {
            edge_count++;
            if(seen[a][b])continue;
            vector<int> face;int u=a,w=b;
            do {
                assert(!seen[u][w]);seen[u][w]=true;face.push_back(u);
                auto &r=rotation[w];auto it=find(r.begin(),r.end(),u);assert(it!=r.end());
                int next=r[(it-r.begin()+1)%r.size()];u=w;w=next;
            } while(u!=a||w!=b);
            ++face_count;
            if(face.size()==8) {assert(boundary.empty());boundary=face;}
            else assert(face.size()==3);
        }
        assert(boundary.size()==8&&n-edge_count/2+face_count==2);
        assert(edge_count/2==3*n-11);
        int named[13];fill(named,named+13,-1);
        for(int i=0;i<8;++i) {assert(named[boundary[i]]==-1);named[boundary[i]]=i;}
        int next=8;for(int i=0;i<n;++i)if(named[i]<0)named[i]=next++;
        for(auto &a:adj)a.clear();
        for(int i=0;i<n;++i)for(int j:rotation[i])adj[named[i]].push_back(named[j]);
        for(int i=0;i<h;++i)ord[i]=8+i;
        sort(ord,ord+h,[](int a,int b){
            int da=0,db=0;for(int w:adj[a])da+=(w<8?20:1);for(int w:adj[b])db+=(w<8?20:1);
            return da!=db?da>db:a<b;
        });
        int counts[274];
        for(int r=0;r<274;++r) {
            fill(colour,colour+13,-1);copy(rows[r],rows[r]+8,colour);
            bool ok=true;
            for(int i=0;i<8;++i)for(int j:adj[i])if(j<8&&colour[i]==colour[j])ok=false;
            counts[r]=ok?count_lifts(0):0;assert(counts[r]<=1024);
            out.put(counts[r]&255);out.put(counts[r]>>8);
            empty+=counts[r]==0;lifts+=counts[r];
        }
        for(int q=0;q<8;++q)for(int t=0;t<16;++t) {
            int hit=0;for(int r=0;r<274;++r)hit+=(counts[r]>0&&upper[q][t][r]);
            if(hit<minima[q]){minima[q]=hit;witness[q]=total;witness_transform[q]=t;}
            rejects[q]+=hit==0;
        }
        ++total;
    }
    stats<<"{\"graphs\":"<<total<<",\"fibres\":"<<total*274<<",\"empty_fibres\":"<<empty
         <<",\"full_lifts\":"<<lifts<<",\"queries\":[";
    for(int q=0;q<8;++q){if(q)stats<<',';stats<<"{\"minimum_intersection\":"<<minima[q]
        <<",\"witness_graph_index\":"<<witness[q]<<",\"witness_transform\":"<<witness_transform[q]
        <<",\"rejecting_orientations\":"<<rejects[q]<<'}';}
    stats<<"]}\n";
    cerr<<total<<" graphs, "<<total*274<<" fibres, "<<lifts<<" full lifts\n";
}
