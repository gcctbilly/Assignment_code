#include <iostream>
#include "Course.h"
#include <string>
#include <vector>
#include <fstream> 
#include "HASH_NODE.h"
#include <iomanip>

using namespace std;


const int COURSE_SIZE = 83;
Course courseList[COURSE_SIZE];

const int HASH_SIZE = 111;
HASH_NODE* hashTable[HASH_SIZE];

struct course{
    string s_courseID;
    string  s_courseName;
    string s_preRequisite;
    string s_creditValue;
    string s_link;
};

struct RESULT{
    Course result_course;
    int show_times = 0;
    RESULT* next = NULL;
};


//data input
void ini();
string readInfor(int);
course informationProcess(string);
string changeToLower(string source);

//data search
int Hash(string str); // input a word and return the hash number of the word 
void iniHashTable(); // initiallize the HashTable
string* keyWordProcess(string keyword,int& wordNumber); // divided the key words into different word part and return the link of the Dynamic array
RESULT* loadResult(RESULT* resultHead, HASH_NODE* node); // input the head of result and load answer to the result
RESULT *hashSearch(string keyword); // input keywords and return the result link list that conatin the course and it showtimes
void add(string word, int index); // add one word to the hash table
vector<string> split(const string& str); 


//data output
void printResult(RESULT*);




int main(){
     
    ini();
    iniHashTable();
    
    //introduction information
    //request for input
    string keyword; string next;
    RESULT* result;
    do{
        
        cout<<"Welcome to the course search application!"<<endl;
        cout<<"Please input keyword(s) of the course(s) you want to search for:"<<endl;
        getline(cin,keyword,'\n');
        result=hashSearch(keyword);
        printResult(result);


        cout<<"Do you want to search for other courses?('Y' for yes and press any other key for no)"<<endl;
        getline(cin,next);
    }while(next == "Y");
 

    return 0;
}






// data input
//initialize all courses
void ini(){
    for(int i=0;i<COURSE_SIZE;i++){
        //get information from the document
        string inforString=readInfor(i+2);
        course inforStruct=informationProcess(inforString);
        
        Course newCourse=Course();
        newCourse.setValue(inforStruct.s_courseID,inforStruct.s_courseName,inforStruct.s_preRequisite,inforStruct.s_creditValue,inforStruct.s_link);
        courseList[i]=newCourse;
    }

}

//read from document
string readInfor(int sequenceNum){
    ifstream  myfile;
    myfile.open("C:\\Users\\15477\\Desktop\\G19\\data.tsv", ios::out | ios::in );

    if(!myfile.is_open()) {
        cout << "open false";
    }
    
    string result;

    for(int i=0;i<sequenceNum;i++){
        getline(myfile,result);
    }
    return result;
}

//deal with "1  COMP1011   Programming Fundamentals    Null    3   https://www.comp.polyu.edu.hk/files/COMP1011_Programming_Fundamentals_Dec2018.pdf"
course informationProcess(string infor){
    
    
    string cid;
    string cname;
    string cpre;
    string ccredit;
    string clink;

    size_t n = infor.find("\t");
    //level
    string level = infor.substr(0,n);

    infor = infor.substr(n + 1);
    n = infor.find("\t");
    //course id
    cid = infor.substr(0, n);

    infor = infor.substr(n + 1);
    n = infor.find("\t");
    //course name
    cname = infor.substr(0, n);

    infor = infor.substr(n + 1);
    n = infor.find("\t");
    //pre-requisite
    cpre = infor.substr(0, n);

    infor = infor.substr(n + 1);
    n = infor.find("\t");
    //credit value
    ccredit = infor.substr(0, n);
    
    infor = infor.substr(n + 1);
    n = infor.find("\t");
    //link
    clink = infor.substr(0, n);

    course a;
    a.s_courseID=cid;
    a.s_courseName=cname;
    a.s_preRequisite=cpre;
    a.s_creditValue=ccredit;
    a.s_link=clink;

    return a;
}


string changeToLower(string source) {
    string result = source;
    for(int i = 0; i<source.length(); i++) {
        result[i] = tolower(source[i]);
    }
    return result;
}



// data search
// compute the hash code
int Hash(string str)
{
   int seed = 131;
   unsigned int hash = 0;

   for(int i = 0; i < str.length(); i++)
   {
      hash = (hash * seed) + str[i];
   }

   return hash%HASH_SIZE;
}

//create a hash table
void iniHashTable(){
     for(int i=0;i<111;i++){ 
        HASH_NODE* temp= new HASH_NODE();
        hashTable[i]= temp;
    }

    for(int i=0;i<83;i++){
        Course currentCourse=courseList[i];
        string currentCourseName=courseList[i].getCourseName();
        vector<string> elements=split(currentCourseName);

        vector<string>::iterator it;
        for(it=elements.begin();it!=elements.end();it++){
            add(*it,i);
        }

    }
}

// process user's input and divided into different words
string* keyWordProcess(string keyword, int& wordNumber) {
    wordNumber++;
    char next;
    int i = 0;

    //remove started blank and end blank
    keyword.erase(0,keyword.find_first_not_of(" "));
    keyword.erase(keyword.find_last_not_of(" ")+1);

    // if their is no key word return null
    if(i == keyword.length()) {
        return NULL;
    }

    keyword = changeToLower(keyword);
    
    // cout word number;
    while(i < keyword.length()) {
        if(keyword[i] == ' ') {
            wordNumber++;
            while(keyword[i+1] == ' ' && (i+1 < keyword.length())) {
                i++;
            } // skip blank space if necessary
        }
        i++;
    }

    string* wordList = new string[wordNumber];

    // ini the word list
    for(int i = 0; i < wordNumber; i++) {
        wordList[i] = "";
    }

    int wordindex = 0;
    int index = 0;


    // add word to word list;
    while(index < keyword.length()) {
        if(keyword[index] == ' ') {
            while(keyword[index+1] == ' ' && (index+1 < keyword.length())) {
                index++;
            } // skip blank space if necessary
            index++;
            wordindex++; // move to next word
        }
        else {
            wordList[wordindex] = wordList[wordindex] + keyword[index];
            index++;

        }
    }

    return wordList;

}

// load the result node into result link list
RESULT* loadResult(RESULT* resultHead, HASH_NODE* node) {
    COURSE_INDEX* currentCouresIndexPtr = node -> getCourseIDPtr();
    
    // if it is the first result
    if(resultHead -> show_times == 0) {

        int courseID = currentCouresIndexPtr -> course_index;
        resultHead -> result_course = courseList[courseID];
        resultHead -> show_times =  resultHead -> show_times + 1;

        currentCouresIndexPtr  = currentCouresIndexPtr -> next; //move to next ID

        // look up all the course id about this word.
        while(currentCouresIndexPtr != NULL) {
            bool needNew = true;
            RESULT* currentResult = resultHead;
            // look up all the course in the result
            while(currentResult != NULL) {
                // judeg if there is the same coure in the result
                if(currentResult -> result_course.getCourseName() ==  courseList[currentCouresIndexPtr -> course_index].getCourseName()) {
                    currentResult -> show_times = currentResult -> show_times + 1;
                    needNew = false;
                    break;
                }
                currentResult = currentResult ->next;
            }
            
            //if no same word in the result
            if(needNew){
                currentResult = new RESULT();
                // add information to new result
                currentResult -> result_course = courseList[currentCouresIndexPtr -> course_index];
                currentResult -> show_times = currentResult -> show_times + 1;

                //add new result to the total result
                RESULT* tempPtr = resultHead;
                resultHead = currentResult;
                resultHead -> next = tempPtr;
            }
            currentCouresIndexPtr = currentCouresIndexPtr ->next;

        }
    }
    else {
        // look up all the course ID;
        while(currentCouresIndexPtr != NULL) {
            bool needNew = true;
            RESULT* currentResult = resultHead;
            // look up all the course in the result
            while(currentResult != NULL) {
                // judeg if there is the same coure in the result
                if(currentResult -> result_course.getCourseName() ==  courseList[currentCouresIndexPtr -> course_index].getCourseName()) {
                    currentResult -> show_times = currentResult -> show_times + 1;
                    needNew = false;
                    break;
                }
                currentResult = currentResult ->next;
            }

            //if no same word in the result
            if(needNew){
                currentResult = new RESULT();
                // add information to new result
                currentResult -> result_course = courseList[currentCouresIndexPtr -> course_index];
                currentResult -> show_times = currentResult -> show_times + 1;

                //add new result to the total result
                RESULT* tempPtr = resultHead;
                resultHead = currentResult;
                resultHead -> next = tempPtr;
            }
            currentCouresIndexPtr = currentCouresIndexPtr ->next;

        }

    }
    return resultHead;

}

//search the hash node contain this keyword
RESULT *hashSearch(string keyword){
    int wordNumber = 0;
    RESULT* resultHead = new RESULT();
    string* wordList = keyWordProcess(keyword, wordNumber); // return dynamic string list with lower words
    //look up all the word that user input
    for(int i = 0; i < wordNumber; i++) {
        int hashNumber = Hash(wordList[i]);
        HASH_NODE* hashHead = hashTable[hashNumber];
        while(hashHead != NULL) {
            if(hashHead -> getWord() == wordList[i]) {
                resultHead = loadResult(resultHead, hashHead);
            }
            hashHead = hashHead -> next;
        }
    }
    return resultHead; 
}

// add a word to the hash function
void add(string word, int index){
    //change the word to lower
    word = changeToLower(word);
    int hashCode=Hash(word);
    bool needAdd = true;
    HASH_NODE* current=hashTable[hashCode];

    // jude whether it is the first node
    if(current ->getWord() == "") {
        COURSE_INDEX* newCourseIndexPtr = new COURSE_INDEX();
        newCourseIndexPtr -> course_index = index;
        current ->setHashNode(word, newCourseIndexPtr);
    }
    else {
        //look up this node which has the same hash code
        while(current != NULL) {
            //judge whether it has the same word in this node. If it has, extent the course index link list about this word
            if(current -> getWord() == word) {
                COURSE_INDEX* newCourseIndexPtr = new COURSE_INDEX();
                newCourseIndexPtr ->course_index = index;
                COURSE_INDEX* temp = current -> getCourseIDPtr();
                current ->setCourseIndex(newCourseIndexPtr);
                current -> getCourseIDPtr() ->next = temp;
                needAdd = false;
                break;
            }
            current = current -> next;
        }
        // if there is no same word add a new node about this hash code
        if(needAdd) {
            HASH_NODE* temp = hashTable[hashCode];
            HASH_NODE* newHashNode = new HASH_NODE();
            COURSE_INDEX* newCourseIndexPtr = new COURSE_INDEX();
            newCourseIndexPtr -> course_index = index;
            newHashNode ->setHashNode(word, newCourseIndexPtr);
            newHashNode -> next = temp;
            hashTable[hashCode] = newHashNode;           

        }
    }
    

}

vector<string> split(const string& str)
{
    vector<string> tokens;
    size_t prev = 0, pos = 0;
    do
    {
        pos = str.find(" ", prev);
        if (pos == string::npos) pos = str.length();
        string token=str.substr(prev, pos - prev);

        //If there is a comma
        
        bool comma = false;
        for (int i = 0; i < token.length(); i++) {
            if (token[i] == ',') {
                token = token.substr(0, token.length()-1);
                comma = true;
            }
        }
      
        
        if (!token.empty()) tokens.push_back(token);
        prev = pos + 1;
        
    } while (pos < str.length() && prev < str.length());
    return tokens;
}

//data output

void printResult(RESULT* result){
    //print the columns line
    cout << std::left << setw(14) << "Course ID" << setw(51) << "Course Name" <<setw(28) << "Pre-requisite" <<setw(17) << "credit value" << setw(9)<< "link" << endl;
    //sorting
    RESULT sortedResultList[COURSE_SIZE];
    int index = 0;

    if(result -> show_times != 0) {
        while (result != NULL) {
        sortedResultList[index++] = *result;
        result = result->next;
        }
    }


    for (int i = 0; i < index; i++) {
        for (int j = i + 1; j < index; j++) {
            if (sortedResultList[i].show_times <sortedResultList[j].show_times) {
                RESULT temp = sortedResultList[i];
                sortedResultList[i] = sortedResultList[j];
                sortedResultList[j] = temp;
            }
        }
    }


    for(int i=0;i<index;i++){
       cout<< std::left << setw(14)<< sortedResultList[i].result_course.getCourseID() << setw(51)
           << sortedResultList[i].result_course.getCourseName()<< setw(28)
           << sortedResultList[i].result_course.getPreRequisite()<< setw(17)
           << sortedResultList[i].result_course.getCreditValue()<< setw(9)
           << sortedResultList[i].result_course.getLink()
           <<endl;
        
    }

    if(index == 0){
        cout << endl;
        cout<<"No courses have been found!"<<endl;
    }

    
}