// Unit-incidence and repeated-template kernels for the frozen W7 cone.
// Numerical discovery only. Original certificate coordinates are unchanged.
#include <cstdint>
#include <algorithm>

extern "C" {
void unit_sum(int n, const int32_t* ptr, const int32_t* ind,
              const double* x, double* y) {
    for (int r = 0; r < n; ++r) {
        double s = 0;
        for (int p = ptr[r]; p < ptr[r+1]; ++p) s += x[ind[p]];
        y[r] = s;
    }
}

// block metadata: nr,nc,ng,rp,ri,cp,ci,rm,cm offsets into shared arrays.
// Coefficients are all 1. Each block occurs ng times with distinct variables.
void template_sum(int nb, const int32_t* meta,
                  const int32_t* rptr, const int32_t* rind,
                  const int32_t* cptr, const int32_t* cind,
                  const int32_t* rows, const int32_t* cols,
                  int transpose, const double* x, double* y,
                  double* packed, double* sums) {
    for (int b = 0; b < nb; ++b) {
        const int32_t* m = meta + 9*b;
        const int nr=m[0], nc=m[1], ng=m[2];
        const int ni=transpose ? nr : nc, no=transpose ? nc : nr;
        const int32_t* ip = transpose ? cptr+m[5] : rptr+m[3];
        const int32_t* ix = transpose ? cind+m[6] : rind+m[4];
        const int32_t* gather = transpose ? rows+m[7] : cols+m[8];
        const int32_t* scatter = transpose ? cols+m[8] : rows+m[7];
        for (int j=0; j<ni*ng; ++j) packed[j]=x[gather[j]];
        std::fill(sums, sums+no*ng, 0.0);
        for (int r=0; r<no; ++r) {
            double* dst=sums+r*ng;
            for (int p=ip[r]; p<ip[r+1]; ++p) {
                const double* src=packed+ix[p]*ng;
                for (int g=0; g<ng; ++g) dst[g] += src[g];
            }
        }
        for (int j=0; j<no*ng; ++j) y[scatter[j]]=sums[j];
    }
}

// A = [D; selected Q]. Q x = 2 P Z; recover Z = h_ref/2 separately.
void project(int ns, const int32_t* ref, const double* h,
             int nl, const int32_t* pp, const int32_t* pi,
             const int32_t* pv, double* out) {
    for (int s=0; s<ns; ++s) {
        int a=0;
        for (int p=0; p<3; ++p) if (p!=ref[s])
            out[2*s+a++]=h[3*s+p]-h[3*s+ref[s]];
    }
    for (int l=0; l<nl; ++l) {
        double v=0;
        for (int p=pp[l]; p<pp[l+1]; ++p) {
            const int s=pi[p];
            v += pv[p]*h[3*s+ref[s]];
        }
        out[2*ns+l]=v;
    }
}

void lift_adjoint(int ns, const int32_t* ref, const double* y,
                  int nl, const int32_t* pp, const int32_t* pi,
                  const int32_t* pv, double* h) {
    for (int s=0; s<ns; ++s) {
        int a=0;
        for (int p=0; p<3; ++p) if (p!=ref[s]) h[3*s+p]=y[2*s+a++];
        h[3*s+ref[s]]=-y[2*s]-y[2*s+1];
    }
    for (int l=0; l<nl; ++l) {
        const double v=y[2*ns+l];
        for (int p=pp[l]; p<pp[l+1]; ++p) {
            const int s=pi[p];
            h[3*s+ref[s]] += pv[p]*v;
        }
    }
}
}
