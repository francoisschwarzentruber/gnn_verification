#define Nbound 2
unsigned int N = Nbound; //number of vertices
#include "typecharsaturation.h"
#include "quantlogic.h"

int main()
  {
  testNumber();
  for(int N1 = 1; N1 <= Nbound; N1++)
  {
    N = N1;
    unknownGraph();
    feature(x1);
    unknownFeature(x1);
    feature(x2);
    unknownFeature(x2);
    __ESBMC_assume(x1[0] == 1);
    __ESBMC_assume(x2[0] == 2);
    feature(x3);
    feature(x4);
    feature(x5);
    feature(x6);
    agg(x3, x1);
    aggG(x5, x1);
    agg(x4, x2);
    aggG(x6, x2);
    feature(x7);
    mul(x7, 1, x1);
    mul(x7, 2, x2);
    mul(x7, 0, x3);
    mul(x7, 0, x4);
    mul(x7, 0, x5);
    mul(x7, 0, x6);
    addCte(x7, 5);
    ReLUp(x7, x7, 6);
    assert(x7[0] == 0);
  }
  return 0;
}
