// Independent C++ cross-check of the reduced C5 cell enumeration (K_k = K_5), multithreaded.
//
//   g++ -O2 -std=c++17 -pthread -o c5_crosscheck c5_crosscheck.cpp
//   ./c5_crosscheck --k 6 --sym none --order within_first --threads 30 --prefix-depth 16 > out.json
//
// Mirrors scripts/c5_k6_crosscheck.py: same universe (ordered C5, k interior vertices, chords, apex-planar),
// R1 (interior degree >= 4 at the leaf) always, optional SYM canonicalisation (none / count / nonincreasing /
// nondecreasing on the five-bit attachment masks), configurable edge order.  Planarity is Boost's
// Boyer–Myrvold test (independent of the rustworkx Left–Right test used by production).  Σ is computed by
// plain backtracking on the interior colours for each of the ten boundary patterns.
//
// Output: one JSON object with search statistics and, per distinct Σ (ten-bit mask in library pattern
// order), the survivor count and the lexicographically smallest witness edge list.
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/boyer_myrvold_planar_test.hpp>
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <mutex>
#include <string>
#include <thread>
#include <vector>

using Graph = boost::adjacency_list<boost::vecS, boost::vecS, boost::undirectedS>;
typedef std::pair<int,int> Edge;
typedef unsigned long long u64;

static int K, N, E, APEX;
static std::string SYM, ORDER;
static std::vector<Edge> EDGES;
static std::vector<u64> TOUCH;               // per interior vertex: bits of its edges
static std::vector<std::array<int,5>> ATTPOS; // per interior vertex: edge index of (i, x)
static std::vector<std::array<int,5>> REPS;   // ten boundary patterns, sorted normalised tuples

static void build_reps() {
    std::vector<std::array<int,5>> all;
    for (int code = 0; code < 1024; ++code) {
        std::array<int,5> b; int t = code;
        for (int i = 0; i < 5; ++i) { b[i] = t & 3; t >>= 2; }
        bool ok = true;
        for (int i = 0; i < 5; ++i) if (b[i] == b[(i + 1) % 5]) ok = false;
        if (!ok) continue;
        std::array<int,5> n; int names[4] = {-1,-1,-1,-1}; int next = 0;
        for (int i = 0; i < 5; ++i) { if (names[b[i]] < 0) names[b[i]] = next++; n[i] = names[b[i]]; }
        all.push_back(n);
    }
    std::sort(all.begin(), all.end());
    all.erase(std::unique(all.begin(), all.end()), all.end());
    REPS = all;
    if (REPS.size() != 10) { fprintf(stderr, "REPS size %zu\n", REPS.size()); exit(1); }
}

static void build_edges() {
    const Edge CH[5] = {{0,2},{0,3},{1,3},{1,4},{2,4}};
    EDGES.assign(CH, CH + 5);
    auto x = [](int m) { return 5 + m; };
    if (ORDER == "production") {
        for (int m = 0; m < K; ++m) { for (int i = 0; i < 5; ++i) EDGES.push_back({i, x(m)}); for (int l = 0; l < m; ++l) EDGES.push_back({x(l), x(m)}); }
    } else if (ORDER == "within_first") {
        for (int m = 0; m < K; ++m) { for (int l = 0; l < m; ++l) EDGES.push_back({x(l), x(m)}); for (int i = 0; i < 5; ++i) EDGES.push_back({i, x(m)}); }
    } else if (ORDER == "attach_first") {
        for (int m = 0; m < K; ++m) for (int i = 0; i < 5; ++i) EDGES.push_back({i, x(m)});
        for (int m = 0; m < K; ++m) for (int l = 0; l < m; ++l) EDGES.push_back({x(l), x(m)});
    } else if (ORDER == "reversed") {
        for (int m = K - 1; m >= 0; --m) { for (int i = 4; i >= 0; --i) EDGES.push_back({i, x(m)}); for (int l = m + 1; l < K; ++l) EDGES.push_back({x(m), x(l)}); }
    } else { fprintf(stderr, "bad order\n"); exit(1); }
    E = (int)EDGES.size();
    TOUCH.assign(K, 0); ATTPOS.assign(K, {});
    for (int j = 0; j < E; ++j) {
        auto [u, v] = EDGES[j];
        if (u >= 5) TOUCH[u - 5] |= 1ULL << j;
        if (v >= 5) TOUCH[v - 5] |= 1ULL << j;
        if (u < 5 && v >= 5) ATTPOS[v - 5][u] = j;
    }
}

static inline int popc(u64 x) { return __builtin_popcountll(x); }

static inline void att_bounds(u64 mask, int e, int m, int& lo, int& hi) {
    lo = 0; hi = 0;
    for (int i = 0; i < 5; ++i) {
        int j = ATTPOS[m][i];
        if (j < e) { if (mask >> j & 1) lo |= 1 << i; } else hi |= 1 << i;
    }
    hi |= lo;
}

static bool viable(u64 mask, int e) {
    u64 undecided = (e >= 64) ? 0 : ~((1ULL << e) - 1);
    for (int m = 0; m < K; ++m)
        if (popc(mask & TOUCH[m]) + popc(TOUCH[m] & undecided) < 4) return false;
    if (SYM == "none") return true;
    for (int m = 1; m < K; ++m) {
        int lo1, hi1, lo2, hi2;
        att_bounds(mask, e, m - 1, lo1, hi1);
        att_bounds(mask, e, m, lo2, hi2);
        if (SYM == "count") { if (popc(lo2) > popc(hi1)) return false; }
        else if (SYM == "nonincreasing") { if (lo2 > hi1) return false; }
        else if (SYM == "nondecreasing") { if (hi2 < lo1) return false; }
    }
    return true;
}

// ---------------------------------------------------------------- Σ by backtracking
struct Sigma {
    int adj[16][16]; int deg[16]; int col[16]; int order[16];
    bool extend(int i) {
        if (i == K) return true;
        int v = order[i];
        for (int c = 0; c < 4; ++c) {
            bool ok = true;
            for (int t = 0; t < deg[v]; ++t) if (col[adj[v][t]] == c) { ok = false; break; }
            if (!ok) continue;
            col[v] = c; if (extend(i + 1)) return true; col[v] = -1;
        }
        return false;
    }
    int eval(u64 mask) {
        for (int v = 0; v < N; ++v) deg[v] = 0;
        auto add = [&](int u, int v) { adj[u][deg[u]++] = v; adj[v][deg[v]++] = u; };
        for (int i = 0; i < 5; ++i) add(i, (i + 1) % 5);
        for (int j = 0; j < E; ++j) if (mask >> j & 1) add(EDGES[j].first, EDGES[j].second);
        for (int m = 0; m < K; ++m) order[m] = 5 + m;
        std::sort(order, order + K, [&](int a, int b) { return deg[a] > deg[b]; });
        int bits = 0;
        for (int j = 0; j < 10; ++j) {
            for (int i = 0; i < 5; ++i) col[i] = REPS[j][i];
            for (int m = 0; m < K; ++m) col[5 + m] = -1;
            bool ok = true;
            for (int u = 0; u < 5 && ok; ++u) for (int t = 0; t < deg[u]; ++t) { int v = adj[u][t]; if (v < 5 && col[v] == col[u]) { ok = false; break; } }
            if (ok && extend(0)) bits |= 1 << j;
        }
        return bits;
    }
};

// ---------------------------------------------------------------- DFS worker
struct Cell { u64 count = 0; int wbits = 99; u64 wmask = 0; };
struct Stats { u64 nodes = 0, survivors = 0, pruned = 0, nonplanar = 0, skipped = 0; };

struct Worker {
    Graph g; Sigma sig; Stats st; std::map<int, Cell> cells;
    Worker() : g(N) {
        for (int i = 0; i < 5; ++i) boost::add_edge(i, (i + 1) % 5, g);
        for (int i = 0; i < 5; ++i) boost::add_edge(APEX, i, g);
    }
    bool planar() { return boost::boyer_myrvold_planarity_test(g); }
    void leaf(u64 mask) {
        if (!viable(mask, E)) return;
        st.survivors++;
        int s = sig.eval(mask);
        Cell& c = cells[s];
        c.count++;
        int pb = popc(mask);
        if (pb < c.wbits || (pb == c.wbits && mask < c.wmask)) { c.wbits = pb; c.wmask = mask; }
    }
    // `bad`: edges already known to make this node's graph nonplanar.  Nonplanarity is monotone under
    // supergraphs, so descendants skip them without a test.  Every candidate edge is tested at this node
    // before any child is entered, so the children inherit the complete bad set (node/survivor counts and
    // the visited tree are unchanged; nonplanar + skipped equals the single-pass nonplanar count).
    void dfs(u64 mask, int start, u64 bad) {
        st.nodes++;
        leaf(mask);
        u64 ok = 0; int stop = E;
        for (int e = start; e < E; ++e) {
            if (!viable(mask, e)) { st.pruned++; stop = e; break; }
            if (bad >> e & 1) { st.skipped++; continue; }
            auto [u, v] = EDGES[e];
            boost::add_edge(u, v, g);
            if (planar()) ok |= 1ULL << e; else { st.nonplanar++; bad |= 1ULL << e; }
            boost::remove_edge(u, v, g);
        }
        for (int e = start; e < stop; ++e) {
            if (!(ok >> e & 1)) continue;
            auto [u, v] = EDGES[e];
            boost::add_edge(u, v, g);
            dfs(mask | (1ULL << e), e + 1, bad);
            boost::remove_edge(u, v, g);
        }
    }
    void task(u64 mask, int start) {
        for (int j = 0; j < start; ++j) if (mask >> j & 1) boost::add_edge(EDGES[j].first, EDGES[j].second, g);
        dfs(mask, start, 0);
        for (int j = 0; j < start; ++j) if (mask >> j & 1) boost::remove_edge(EDGES[j].first, EDGES[j].second, g);
    }
};

static std::vector<u64> prefix_nodes(int depth) {
    Worker w; std::vector<u64> out;
    std::function<void(u64,int)> rec = [&](u64 mask, int start) {
        if (viable(mask, depth)) out.push_back(mask);
        for (int e = start; e < depth; ++e) {
            if (!viable(mask, e)) return;
            auto [u, v] = EDGES[e];
            boost::add_edge(u, v, w.g);
            if (w.planar()) rec(mask | (1ULL << e), e + 1);
            boost::remove_edge(u, v, w.g);
        }
    };
    rec(0, 0);
    return out;
}

int main(int argc, char** argv) {
    K = 6; SYM = "none"; ORDER = "within_first"; int threads = 30, depth = 16;
    for (int i = 1; i + 1 < argc; i += 2) {
        std::string a = argv[i];
        if (a == "--k") K = atoi(argv[i+1]); else if (a == "--sym") SYM = argv[i+1]; else if (a == "--order") ORDER = argv[i+1];
        else if (a == "--threads") threads = atoi(argv[i+1]); else if (a == "--prefix-depth") depth = atoi(argv[i+1]);
        else { fprintf(stderr, "unknown arg %s\n", argv[i]); return 1; }
    }
    if (SYM != "none" && SYM != "count" && SYM != "nonincreasing" && SYM != "nondecreasing") { fprintf(stderr, "bad sym\n"); return 1; }
    N = 5 + K + 1; APEX = 5 + K;
    build_reps(); build_edges();
    if (depth > E) depth = E;
    auto t0 = std::chrono::steady_clock::now();
    std::vector<u64> nodes = prefix_nodes(depth);
    std::sort(nodes.begin(), nodes.end(), [](u64 a, u64 b) { return popc(a) < popc(b); });   // few prefix edges = big subtree: schedule first
    std::atomic<size_t> next(0); std::atomic<u64> done(0);
    std::vector<Worker*> workers(threads);
    std::vector<std::thread> pool;
    for (int t = 0; t < threads; ++t) {
        workers[t] = new Worker();
        pool.emplace_back([&, t]() {
            for (;;) {
                size_t i = next.fetch_add(1);
                if (i >= nodes.size()) break;
                workers[t]->task(nodes[i], depth);
                u64 d = ++done;
                if (d % 2000 == 0 || d == nodes.size()) {
                    double s = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
                    fprintf(stderr, "k=%d sym=%s order=%s tasks=%llu/%zu seconds=%.1f\n", K, SYM.c_str(), ORDER.c_str(), d, nodes.size(), s);
                }
            }
        });
    }
    for (auto& th : pool) th.join();
    Stats st; std::map<int, Cell> cells;
    for (Worker* w : workers) {
        st.nodes += w->st.nodes; st.survivors += w->st.survivors; st.pruned += w->st.pruned; st.nonplanar += w->st.nonplanar; st.skipped += w->st.skipped;
        for (auto& [s, c] : w->cells) {
            Cell& m = cells[s]; m.count += c.count;
            if (c.wbits < m.wbits || (c.wbits == m.wbits && c.wmask < m.wmask)) { m.wbits = c.wbits; m.wmask = c.wmask; }
        }
    }
    double secs = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    printf("{\n \"k\": %d, \"sym\": \"%s\", \"order\": \"%s\", \"threads\": %d, \"prefix_depth\": %d, \"prefix_tasks\": %zu,\n", K, SYM.c_str(), ORDER.c_str(), threads, depth, nodes.size());
    printf(" \"boost_version\": %d, \"planarity\": \"boost::boyer_myrvold_planarity_test\",\n", BOOST_VERSION);
    printf(" \"search\": {\"nodes\": %llu, \"survivors\": %llu, \"pruned\": %llu, \"nonplanar\": %llu, \"skipped_known_nonplanar\": %llu, \"seconds\": %.1f},\n", st.nodes, st.survivors, st.pruned, st.nonplanar, st.skipped, secs);
    printf(" \"edges\": [");
    for (int j = 0; j < E; ++j) printf("%s[%d,%d]", j ? "," : "", EDGES[j].first, EDGES[j].second);
    printf("],\n \"distinct_sigma\": %zu,\n \"cells\": {", cells.size());
    bool first = true;
    for (auto& [s, c] : cells) {
        printf("%s\n  \"%d\": {\"count\": %llu, \"witness_mask\": %llu, \"edges\": [", first ? "" : ",", s, c.count, c.wmask);
        bool f2 = true;
        for (int j = 0; j < E; ++j) if (c.wmask >> j & 1) { printf("%s[%d,%d]", f2 ? "" : ",", EDGES[j].first, EDGES[j].second); f2 = false; }
        printf("]}");
        first = false;
    }
    printf("\n }\n}\n");
    return 0;
}
