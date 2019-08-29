#include <string>
#include <vector>
#include <math.h>

// https://www.codewars.com/kata/51ba717bb08c1cd60f00002f

using namespace std;

string range_extraction(vector<int> args) {
	string ret = "";
	for (int i = 0; i < args.size(); ++i)
	{
		if (max(args[i] - args[i+1], args[i+1] - args[i]) > 1 ){
			ret.append(to_string(args[i]) + ",");
			continue;
		}
		for (int j = i+1; j <= args.size(); ++j)
		{
			if (max(args[j-1] - args[j], args[j] - args[j-1]) != 1) {
				if(max(i - (j-1), (j-1) - i) == 1){
					ret.append(to_string(args[i]) + "," + to_string(args[j-1]) + ",");
				} else {
					ret.append(to_string(args[i]) + "-" + to_string(args[j-1]) + ",");
				}
				i = j-1;
				break;
			}
		}
	}
	ret.pop_back();
	return ret;
}