#include <iostream>
#include <time.h>
#include "Node.h"

using namespace std;

Node::Node() {
    data = rand() % 100;
    before_link = NULL;
    next_link = NULL;
}


void Node::print_list(Node* head) {
    Node* current_link = head;
    while(current_link != NULL) {
        cout << current_link -> data << " ";
        current_link = current_link -> next_link;       
    }
    
}

Node::Node(int number) {
    data = number;
}

int Node::get_data() {
    return data;
}

void creat_list(Node*& head, Node*& end, int size) {
    Node* current_link;
    if(size == 0) {
        head = NULL;
        end = head;
    }
    else{
        head = new Node();
        end = head;

        for(int i = 1; i < size; i++) {
        current_link = new Node();
        current_link -> before_link = end;
        end -> next_link = current_link;
        end = current_link;
        }
    }
    
}

void reverse(Node* head) {
    if(head == NULL) {
        return;
    }
    else {
        // change before_link and next_link of one Node
        Node* temp_link = head -> before_link;
        head -> before_link = head -> next_link;
        head -> next_link = temp_link;
        
        reverse(head -> before_link); // go to next node

        return;

    }
}



int main() {
    srand(time(0));

    int size;
    Node* head;   // point to fist Node
    Node* end;    // point to last Node
    cout << "Please enter the size of the link list: ";
    cin >> size;
    creat_list(head,end,size);
    cout << "The link list is: "; 
    head ->print_list(head);
    cout << endl;
    
    reverse(head);
    
    // change head and end
    Node* temp = head;
    head  = end;
    end = temp;

    cout << "After reverse, the link list is: ";
    head -> print_list(head);
    
    return 0;

}