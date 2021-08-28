#include <iostream>
#include <stdlib.h>

using namespace std;

class Node {
    private:
    int data;

    public:
    Node* before_link;
    Node* next_link;

    Node();

    Node(int number);

    void print_list(Node* head);

    int get_data();
};
