// https://www.codewars.com/kata/two-sum/train/cpp


std::pair<std::size_t, std::size_t> two_sum(const std::vector<int>& numbers, int target) {
	for (int i = 0; i < numbers.size(); ++i)
	{
		for (int j = 0; j < numbers.size(); ++j)
		{
			if(i == j){
				continue;
			}
			if(numbers[i] + numbers[j] == target){
				return {i, j};
			}
		}
	}
}