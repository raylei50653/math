/* Output-only filter: the min4 recursion is unchanged. */
#define FILTER k13_min5_filter
#define SUMMARY k13_filter_summary
static unsigned long long k13_seen = 0, k13_accepted = 0;
static int k13_min5_filter(int nbtot, int nbop, int doflip)
{
    int v;
    (void)nbtot; (void)nbop; (void)doflip;
    ++k13_seen;
    for (v = 0; v < nv; ++v) if (degree[v] < 5) return 0;
    ++k13_accepted;
    return 1;
}
static void k13_filter_summary(void)
{
    fprintf(msgfile, "min4_output_filter_seen=%llu accepted_min5=%llu\n",
            k13_seen, k13_accepted);
}
