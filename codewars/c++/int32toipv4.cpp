// https://www.codewars.com/kata/52e88b39ffb6ac53a400022e/train/cpp

// This is the original code I wrote, below is my refactored code after learning more

std::string uint32_to_ip(uint32_t ip)
{
  std::cout << ip << std::endl;
  std::bitset<32> ipaddrbits (ip);
  std::bitset<32> firstmask  (std::string("11111111000000000000000000000000"));
  std::bitset<32> secondmask (std::string("00000000111111110000000000000000"));
  std::bitset<32> thirdmask  (std::string("00000000000000001111111100000000"));
  std::bitset<32> fourthmask (std::string("00000000000000000000000011111111"));
  std::bitset<32> firstoct   ((ipaddrbits & firstmask) >> 24);
  std::bitset<32> secondoct  ((ipaddrbits & secondmask) >> 16);
  std::bitset<32> thirdoct   ((ipaddrbits & thirdmask) >> 8);
  std::bitset<32> fourthoct  ((ipaddrbits & fourthmask));
  return std::to_string(firstoct.to_ulong()) + "." + std::to_string(secondoct.to_ulong()) + "." + std::to_string(thirdoct.to_ulong()) + "." + std::to_string(fourthoct.to_ulong());
}

using namespace std;
string uint32_to_ip(uint32_t ip){
	int first  = (ip >> 24) & 0xFF;
	int second = (ip >> 16) & 0xFF;
	int third  = (ip >> 8)  & 0xFF;
	int fourth = (ip)       & 0xFF;
	return to_string(first) + "." +to_string(second) + "." + to_string(third) + "." + to_string(fourth);
}

// this one is a good ex of string formatting i need to learn

std::string uint32_to_ip(uint32_t ip)
{
  char result[16] = {0};
  uint8_t *ip_c = (uint8_t *)&ip;
  snprintf(result, sizeof(result), "%d.%d.%d.%d", ip_c[3], ip_c[2], ip_c[1], ip_c[0]);
  return std::string(result);
}

// Libraries are important

#include <arpa/inet.h>

std::string uint32_to_ip(uint32_t ip)
{
    in_addr addr;
    addr.s_addr = htonl(ip);
    return {inet_ntoa(addr)};
}
