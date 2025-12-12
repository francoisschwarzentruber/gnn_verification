#define Nbound 4
unsigned int N = Nbound; //number of vertices
#include "typecharsaturation.h"
#include "quantlogic.h"

int main()
  {
  testNumber();
  for(int N1 = 0; N1 <= Nbound; N1++)
  {
    N = N1;
    unknownGraph();
    feature(x1);
    unknownFeature(x1);
    __ESBMC_assume(x1[0] == 0 || x1[0] == 1);
    __ESBMC_assume(x1[1] == 0 || x1[1] == 1);
    __ESBMC_assume(x1[2] == 0 || x1[2] == 1);
    __ESBMC_assume(x1[3] == 0 || x1[3] == 1);
    feature(x2);
    unknownFeature(x2);
    __ESBMC_assume(x2[0] == 0 || x2[0] == 1);
    __ESBMC_assume(x2[1] == 0 || x2[1] == 1);
    __ESBMC_assume(x2[2] == 0 || x2[2] == 1);
    __ESBMC_assume(x2[3] == 0 || x2[3] == 1);
    feature(x3);
    feature(x4);
    feature(x5);
    feature(x6);
    agg(x3, x1);
    aggG(x5, x1);
    agg(x4, x2);
    aggG(x6, x2);
    feature(x7);
    mul(x7, 8, x1);
    mul(x7, 2, x2);
    mul(x7, 5, x3);
    mul(x7, 7, x4);
    mul(x7, 9, x5);
    mul(x7, 9, x6);
    addCte(x7, 2);
    ReLU(x7, x7);
    feature(x8);
    mul(x8, 4, x1);
    mul(x8, 8, x2);
    mul(x8, 5, x3);
    mul(x8, 5, x4);
    mul(x8, 4, x5);
    mul(x8, 10, x6);
    addCte(x8, 7);
    ReLU(x8, x8);
    feature(x9);
    feature(x10);
    feature(x11);
    feature(x12);
    agg(x9, x7);
    aggG(x11, x7);
    agg(x10, x8);
    aggG(x12, x8);
    feature(x13);
    mul(x13, 8, x7);
    mul(x13, 7, x8);
    mul(x13, 4, x9);
    mul(x13, 9, x10);
    mul(x13, 5, x11);
    mul(x13, 1, x12);
    addCte(x13, 7);
    ReLU(x13, x13);
    feature(x14);
    mul(x14, 1, x7);
    mul(x14, 9, x8);
    mul(x14, 8, x9);
    mul(x14, 5, x10);
    mul(x14, 7, x11);
    mul(x14, 8, x12);
    addCte(x14, 7);
    ReLU(x14, x14);
    assert(x14[0] >= 0);
  }
  return 0;
}
