// Kempe-free C-reducibility screen for the RSST unavoidable configurations.
//
// For a configuration K with free completion S and ring R, A(K) is the set of
// proper 4-colourings of R (modulo all colour permutations) that extend to S.
// A contract X (RSST rules: 1<=|X|<=4, no ring edge, sparse, triad if |X|=4)
// is Kempe-free when every colouring of S whose monochromatic edge set is
// exactly X restricts to a ring colouring in A(K), and at least one such
// colouring exists.  RSST's C-reducibility only asks for the D-closure.
//
// One pass: every ring colouring c outside A(K) is extended over the interior
// allowing monochromatic edges; a completed colouring with monochromatic set
// D kills the contract D.  Partial sets that are not contained in a live
// contract are pruned.  Survivors are then checked for non-vacuity.
//
// Usage: kempe_free_contracts unavoidable.conf [threads]  > results.jsonl
#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <mutex>
#include <set>
#include <sstream>
#include <string>
#include <thread>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using namespace std;
typedef uint64_t u64;

struct Conf {
  string name;
  int n = 0, r = 0, ext = 0, maxcons = 0;
  vector<pair<int, int>> contract;  // 0-indexed vertices
  vector<vector<int>> adj;          // rotation lists, 0-indexed
};

static bool next_nonblank(istream &in, string &line) {
  while (getline(in, line)) {
    if (line.find_first_not_of(" \t\r") != string::npos) return true;
  }
  return false;
}

static bool read_conf(istream &in, Conf &c) {
  string line;
  if (!next_nonblank(in, line)) return false;
  c.name = line.substr(line.find_first_not_of(" \t"));
  while (!c.name.empty() && (c.name.back() == ' ' || c.name.back() == '\r')) c.name.pop_back();
  getline(in, line);
  {
    istringstream s(line);
    s >> c.n >> c.r >> c.ext >> c.maxcons;
  }
  getline(in, line);
  {
    istringstream s(line);
    int k;
    s >> k;
    c.contract.clear();
    for (int i = 0; i < k; i++) {
      int u, v;
      s >> u >> v;
      c.contract.push_back({u - 1, v - 1});
    }
  }
  c.adj.assign(c.n, {});
  for (int i = 0; i < c.n; i++) {
    getline(in, line);
    istringstream s(line);
    int j, d;
    s >> j >> d;
    if (j != i + 1) {
      fprintf(stderr, "bad vertex line in %s\n", c.name.c_str());
      exit(2);
    }
    for (int t = 0; t < d; t++) {
      int w;
      s >> w;
      c.adj[i].push_back(w - 1);
    }
  }
  int seen = 0;
  while (seen < c.n) {  // coordinates
    getline(in, line);
    istringstream s(line);
    long x;
    while (s >> x) seen++;
  }
  return true;
}

struct Graph {
  int n, r, m;                      // m = number of interior vertices
  vector<vector<int>> eid;          // edge id or -1
  vector<pair<int, int>> edges;
  vector<bool> ring_edge;
  vector<array<int, 3>> tris;       // edge ids per triangle
  vector<vector<int>> edge_tris;
  vector<int> order;                // interior order
  vector<vector<pair<int, int>>> back;  // per position: (earlier vertex, edge id)
};

static Graph build(const Conf &c) {
  Graph g;
  g.n = c.n;
  g.r = c.r;
  g.m = c.n - c.r;
  g.eid.assign(c.n, vector<int>(c.n, -1));
  auto add = [&](int u, int v) {
    if (g.eid[u][v] >= 0) return;
    g.eid[u][v] = g.eid[v][u] = (int)g.edges.size();
    g.edges.push_back({min(u, v), max(u, v)});
    g.ring_edge.push_back(u < c.r && v < c.r && ((u + 1) % c.r == v || (v + 1) % c.r == u));
  };
  for (int i = 0; i < c.r; i++) add(i, (i + 1) % c.r);
  for (int v = 0; v < c.n; v++)
    for (int u : c.adj[v]) add(v, u);
  if ((int)g.edges.size() != 3 * c.n - 3 - c.r) {
    fprintf(stderr, "edge count mismatch in %s\n", c.name.c_str());
    exit(2);
  }
  if ((int)g.edges.size() > 64) {
    fprintf(stderr, "too many edges in %s\n", c.name.c_str());
    exit(2);
  }
  set<array<int, 3>> seen;
  for (int v = 0; v < c.n; v++) {
    int d = c.adj[v].size();
    for (int h = 0; h < d; h++) {
      if (v < c.r && h == d - 1) continue;  // outer face at ring vertex
      int u = c.adj[v][h], w = c.adj[v][(h + 1) % d];
      array<int, 3> t = {v, u, w};
      sort(t.begin(), t.end());
      if (seen.count(t)) continue;
      seen.insert(t);
      if (g.eid[t[0]][t[1]] < 0 || g.eid[t[1]][t[2]] < 0 || g.eid[t[0]][t[2]] < 0) {
        fprintf(stderr, "non-triangle in %s\n", c.name.c_str());
        exit(2);
      }
      g.tris.push_back({g.eid[t[0]][t[1]], g.eid[t[1]][t[2]], g.eid[t[0]][t[2]]});
    }
  }
  // Euler check for a near-triangulation with outer face R: F_inner = 2n - 2 - r.
  if ((int)g.tris.size() != 2 * c.n - 2 - c.r) {
    fprintf(stderr, "face count mismatch in %s\n", c.name.c_str());
    exit(2);
  }
  g.edge_tris.assign(g.edges.size(), {});
  for (int t = 0; t < (int)g.tris.size(); t++)
    for (int e : g.tris[t]) g.edge_tris[e].push_back(t);
  vector<bool> done(c.n, false);
  for (int i = 0; i < c.r; i++) done[i] = true;
  for (int step = 0; step < g.m; step++) {
    int best = -1, bscore = -1;
    for (int v = c.r; v < c.n; v++) {
      if (done[v]) continue;
      int s = 0;
      for (int u : c.adj[v]) s += done[u];
      int score = s * 100 + (int)c.adj[v].size();
      if (score > bscore) bscore = score, best = v;
    }
    done[best] = true;
    g.order.push_back(best);
  }
  vector<int> pos(c.n, -1);
  for (int i = 0; i < c.r; i++) pos[i] = -2;  // ring: always earlier
  for (int i = 0; i < g.m; i++) pos[g.order[i]] = i;
  g.back.assign(g.m, {});
  for (int i = 0; i < g.m; i++) {
    int v = g.order[i];
    for (int u : c.adj[v])
      if (pos[u] == -2 || pos[u] < i) g.back[i].push_back({u, g.eid[u][v]});
  }
  return g;
}

static bool triad_ok(const Conf &c, const Graph &g, u64 X) {
  // RSST reduce.c findangles(): a vertex v of K adjacent to >=3 contract ends,
  // and either deg(v)>=6 or some contract end is not adjacent to v.
  vector<int> ends;
  for (int e = 0; e < (int)g.edges.size(); e++)
    if (X >> e & 1) ends.push_back(g.edges[e].first), ends.push_back(g.edges[e].second);
  set<int> endset(ends.begin(), ends.end());
  for (int v = c.r; v < c.n; v++) {
    int a = 0;
    set<int> nb(c.adj[v].begin(), c.adj[v].end());
    for (int u : c.adj[v]) a += endset.count(u);
    if (a < 3) continue;
    if ((int)c.adj[v].size() >= 6) return true;
    for (int x : ends)
      if (!nb.count(x)) return true;
  }
  return false;
}

struct Result {
  string json;
};

struct Worker {
  const Conf &c;
  const Graph g;
  vector<int> col;
  unordered_map<u64, int> cnt;   // subset -> number of live contracts containing it
  unordered_set<u64> live;
  long long nodes = 0;
  bool proper_found = false;
  bool kill_phase = true;

  explicit Worker(const Conf &cc) : c(cc), g(build(cc)), col(cc.n, -1) {}

  bool extends(int p) {
    if (p == g.m) return true;
    int v = g.order[p];
    for (int k = 0; k < 4; k++) {
      bool ok = true;
      for (auto &be : g.back[p])
        if (col[be.first] == k) {
          ok = false;
          break;
        }
      if (!ok) continue;
      col[v] = k;
      if (extends(p + 1)) {
        col[v] = -1;
        return true;
      }
    }
    col[v] = -1;
    return false;
  }

  void insert(u64 X) {
    live.insert(X);
    for (u64 s = X;; s = (s - 1) & X) {
      cnt[s]++;
      if (s == 0) break;
    }
  }
  void erase(u64 X) {
    live.erase(X);
    for (u64 s = X;; s = (s - 1) & X) {
      if (--cnt[s] == 0) cnt.erase(s);
      if (s == 0) break;
    }
  }
  bool in_closure(u64 D) const { return cnt.count(D) > 0; }

  // Extend over the interior; at a leaf with monochromatic set D, call hit(D).
  template <class F>
  void defect_dfs(int p, u64 D, F &hit) {
    nodes++;
    if (live.empty()) return;
    if (p == g.m) {
      if (D == 0) {
        if (kill_phase) proper_found = true;
        return;
      }
      hit(D);
      return;
    }
    int v = g.order[p];
    for (int k = 0; k < 4; k++) {
      u64 nd = D;
      for (auto &be : g.back[p])
        if (col[be.first] == k) nd |= (u64)1 << be.second;
      if (nd != D && !in_closure(nd)) continue;
      col[v] = k;
      defect_dfs(p + 1, nd, hit);
      col[v] = -1;
    }
  }

  string pairs(u64 X) const {
    string s = "[";
    bool first = true;
    for (int e = 0; e < (int)g.edges.size(); e++)
      if (X >> e & 1) {
        if (!first) s += ",";
        first = false;
        s += "[" + to_string(g.edges[e].first + 1) + "," + to_string(g.edges[e].second + 1) + "]";
      }
    return s + "]";
  }
  string colstr(const vector<int> &cc) const {
    string s;
    for (int x : cc) s += char('0' + x);
    return s;
  }

  string run() {
    auto t0 = chrono::steady_clock::now();
    // ring colourings, canonical by first appearance
    vector<vector<int>> rings;
    vector<int> rc(c.r);
    function<void(int, int)> gen = [&](int i, int mx) {
      if (i == c.r) {
        if (rc[c.r - 1] != rc[0]) rings.push_back(rc);
        return;
      }
      for (int k = 0; k <= min(mx + 1, 3); k++) {
        if (i > 0 && k == rc[i - 1]) continue;
        rc[i] = k;
        gen(i + 1, max(mx, k));
      }
    };
    rc[0] = 0;
    gen(1, 0);
    vector<char> good(rings.size());
    int acount = 0;
    for (size_t i = 0; i < rings.size(); i++) {
      for (int j = 0; j < c.r; j++) col[j] = rings[i][j];
      good[i] = extends(0);
      acount += good[i];
    }
    // valid contracts
    vector<int> nonring;
    for (int e = 0; e < (int)g.edges.size(); e++)
      if (!g.ring_edge[e]) nonring.push_back(e);
    vector<int> tri_used(g.tris.size(), 0);
    array<long long, 5> valid_by{0, 0, 0, 0, 0};
    vector<u64> valid;
    function<void(int, int, u64)> choose = [&](int start, int size, u64 X) {
      if (size >= 1) {
        if (size < 4 || triad_ok(c, g, X)) {
          valid.push_back(X);
          valid_by[size]++;
        }
      }
      if (size == 4) return;
      for (int i = start; i < (int)nonring.size(); i++) {
        int e = nonring[i];
        bool ok = true;
        for (int t : g.edge_tris[e])
          if (tri_used[t]) ok = false;
        if (!ok) continue;
        for (int t : g.edge_tris[e]) tri_used[t]++;
        choose(i + 1, size + 1, X | ((u64)1 << e));
        for (int t : g.edge_tris[e]) tri_used[t]--;
      }
    };
    choose(0, 0, 0);
    cnt.reserve(valid.size() * 6);
    for (u64 X : valid) insert(X);
    u64 rsstX = 0;
    for (auto &p : c.contract) {
      int e = g.eid[p.first][p.second];
      if (e < 0) {
        fprintf(stderr, "RSST contract non-edge in %s\n", c.name.c_str());
        exit(2);
      }
      rsstX |= (u64)1 << e;
    }
    bool rsst_valid = rsstX == 0 || live.count(rsstX);
    // kill phase, recording a witness for the RSST contract
    string rsst_witness = "null";
    long long bad = 0;
    for (size_t i = 0; i < rings.size() && !live.empty(); i++) {
      if (good[i]) continue;
      bad++;
      for (int j = 0; j < c.r; j++) col[j] = rings[i][j];
      auto hit = [&](u64 D) {
        if (!live.count(D)) return;
        if (D == rsstX) rsst_witness = "\"" + colstr(col) + "\"";
        erase(D);
      };
      defect_dfs(0, 0, hit);
    }
    long long bad_total = 0;
    for (size_t i = 0; i < rings.size(); i++) bad_total += !good[i];
    bool rsst_kf_nonvacuous = false;
    vector<u64> survivors(live.begin(), live.end());
    // non-vacuity: some colouring with monochromatic set exactly X (ring in A(K))
    set<u64> witnessed;
    kill_phase = false;
    if (!survivors.empty()) {
      for (size_t i = 0; i < rings.size() && !live.empty(); i++) {
        if (!good[i]) continue;
        for (int j = 0; j < c.r; j++) col[j] = rings[i][j];
        auto hit = [&](u64 D) {
          if (!live.count(D)) return;
          witnessed.insert(D);
          erase(D);
        };
        defect_dfs(0, 0, hit);
      }
      live.clear();
      cnt.clear();
    }
    array<long long, 5> kf_by{0, 0, 0, 0, 0}, vac_by{0, 0, 0, 0, 0};
    vector<u64> kf;
    for (u64 X : survivors) {
      int s = __builtin_popcountll(X);
      if (witnessed.count(X)) kf_by[s]++, kf.push_back(X);
      else vac_by[s]++;
    }
    sort(kf.begin(), kf.end(), [](u64 a, u64 b) {
      int pa = __builtin_popcountll(a), pb = __builtin_popcountll(b);
      return pa != pb ? pa < pb : a < b;
    });
    if (rsstX && witnessed.count(rsstX)) rsst_kf_nonvacuous = true;
    int minsize = kf.empty() ? 0 : __builtin_popcountll(kf[0]);
    double secs = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    ostringstream o;
    auto arr = [&](const array<long long, 5> &a) {
      return "[" + to_string(a[1]) + "," + to_string(a[2]) + "," + to_string(a[3]) + "," + to_string(a[4]) + "]";
    };
    o << "{\"name\":\"" << c.name << "\",\"n\":" << c.n << ",\"ring\":" << c.r
      << ",\"ext_claim\":" << c.ext << ",\"A\":" << acount << ",\"ring_colourings\":" << rings.size()
      << ",\"bad\":" << bad_total << ",\"rsst_contract\":" << pairs(rsstX)
      << ",\"rsst_contract_valid\":" << (rsst_valid ? "true" : "false")
      << ",\"rsst_contract_kempe_free\":" << (rsst_kf_nonvacuous ? "true" : "false")
      << ",\"rsst_contract_witness\":" << rsst_witness
      << ",\"valid_by_size\":" << arr(valid_by) << ",\"kempe_free_by_size\":" << arr(kf_by)
      << ",\"vacuous_by_size\":" << arr(vac_by) << ",\"min_kempe_free_size\":" << minsize
      << ",\"kempe_free_examples\":[";
    for (size_t i = 0; i < kf.size() && i < 5; i++) o << (i ? "," : "") << pairs(kf[i]);
    o << "],\"proper_on_bad\":" << (proper_found ? "true" : "false") << ",\"nodes\":" << nodes
      << ",\"seconds\":" << secs << "}";
    return o.str();
  }
};

int main(int argc, char **argv) {
  if (argc < 2) {
    fprintf(stderr, "usage: %s unavoidable.conf [threads] [first] [last]\n", argv[0]);
    return 1;
  }
  ifstream in(argv[1]);
  vector<Conf> confs;
  Conf c;
  while (read_conf(in, c)) confs.push_back(c);
  int threads = argc > 2 ? atoi(argv[2]) : (int)thread::hardware_concurrency();
  int first = argc > 3 ? atoi(argv[3]) : 1;
  int last = argc > 4 ? atoi(argv[4]) : (int)confs.size();
  vector<string> out(confs.size());
  atomic<int> next(first - 1);
  mutex mu;
  vector<thread> pool;
  for (int t = 0; t < threads; t++)
    pool.emplace_back([&]() {
      for (;;) {
        int i = next++;
        if (i >= last) return;
        Worker w(confs[i]);
        string s = w.run();
        lock_guard<mutex> lk(mu);
        out[i] = "{\"index\":" + to_string(i + 1) + "," + s.substr(1);
        fprintf(stderr, "%d %s\n", i + 1, confs[i].name.c_str());
      }
    });
  for (auto &th : pool) th.join();
  for (int i = first - 1; i < last; i++) printf("%s\n", out[i].c_str());
  return 0;
}
