using namespace std;

class Course{
    
    public:
    Course();
    //Course(string courseID,string courseName,string preRequisite,int creditValue,string link);
    void setValue(string courseID,string courseName,string preRequisite,string creditValue,string link);
   

    string getCourseID();
    string getCourseName();
    string getPreRequisite();
    string getCreditValue();
    string getLink();

    Course* next;

    private:
    string m_courseID;
    string  m_courseName;
    string m_preRequisite;
    string m_creditValue;
    string m_link;
};

Course::Course() {
    m_courseName = "";
    m_preRequisite = "";
    m_creditValue = "";
    m_link = "";
    next = NULL;
}

void Course::setValue(string courseID,string courseName,string preRequisite,string creditValue,string link){
    m_courseID=courseID;
    m_courseName=courseName;
    m_preRequisite=preRequisite;
    m_creditValue=creditValue;
    m_link=link;
}

string Course::getCourseID(){
    return m_courseID;
}

string Course::getCourseName() {
    return m_courseName;
}

string Course::getCreditValue() {
    return m_creditValue;
}

string Course::getPreRequisite() {
    return m_preRequisite;
}

string Course::getLink() {
    return m_link;
}


