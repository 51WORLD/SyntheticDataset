#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iomanip>
#include <vector>
#include <math.h>
#include <typeinfo>
using namespace std;

#ifdef _WIN32
	#include<io.h>
#else
	#include <dirent.h> 
#endif

struct PointXYZRGBI
{
	float x, y, z ;       
	uint32_t  rgb;        
	uint8_t intensity,segmentationPath,ring,angle;   
}; 
struct PointXYZI
{
	float x, y, z ;     
	float intensity;   
}; 

void ReadPCDfile(const string& pcdPath, const string& binPath)
{
	ifstream fin(pcdPath, ios::in| ios::binary);  
	if (!fin) {
		cout << "file opens failed" << endl;
		return ;
	}
	char s[11][1024];                         
	uint32_t pointsNumber;                 
	string data_columns_type;            
	string data_type;                   

	cout << "start to read file header....." << endl;
	for (int i = 0; i < 11; ++i){
		fin.getline(s[i],1024);  
		cout << "第" << i + 1 << "行：" << s[i] << endl;
		
		//FIELDS x y z rgb
		if (i == 2) {
			string s2 = s[2];
			size_t pos = s2.find("FIELDS");    
			size_t size = s2.size();          
			data_columns_type = s2.substr(pos + 7, size);
			cout << "data_columns_type:" << data_columns_type << endl;
		}
		if (i == 9) {
			string s9 = s[9], Points_Str;
			size_t pos = s9.find("POINTS");
			size_t size = s9.size();                    
			Points_Str = s9.substr(pos + 7, size);   
			pointsNumber = atoi(Points_Str.c_str());  
			cout << "Points:" << pointsNumber << endl;  
		}
		if (i == 10) {
			string s10 = s[10], DATA_SIZE;
			size_t pos = s10.find("DATA");     
			size_t size = s10.size();         
			data_type = s10.substr(pos + 5, size);
			cout << "data_type:" << data_type << endl;
		}
	}
	cout << "current position of file pointer :" << fin.tellg() << endl;    
	uint32_t pcdHeaderSize = fin.tellg();
	fin.seekg(0, ios::end);    
	uint32_t pointCouldDataSize = uint32_t(fin.tellg()) - pcdHeaderSize;   
	cout<<"pointCouldDataSize:"<<pointCouldDataSize<<endl;
	
	cout << "start to read point ....." << endl;
	vector<int8_t> pointCouldData;
	pointCouldData.resize(pointCouldDataSize);            
	fin.seekg(pcdHeaderSize, ios::beg);     
	if ((data_columns_type == "x y z rgb intensity segmentation ring angle") && (data_type == "binary")){
		fin.read(reinterpret_cast<char*>(pointCouldData.data()), pointCouldDataSize); 
		cout << "curent frame point clound size:" << pointCouldData.size() << endl;
	} 
	else
		cout << "data_type = binary, read failed!" << endl;	
	PointXYZRGBI * pClound = reinterpret_cast<PointXYZRGBI*>(pointCouldData.data());
    PointXYZI* pPointBuffer = (PointXYZI*)malloc(pointsNumber*16);
    PointXYZI* pPointBufferStart=pPointBuffer;

	for (uint32_t i = 0; i < pointsNumber; ++i){
		float d = sqrt(pow(pClound->x, 2) + pow(pClound->y, 2) + pow(pClound->z, 2));
        pPointBuffer->x=pClound->x;
        pPointBuffer->y=pClound->y;
        pPointBuffer->z=pClound->z;
		pPointBuffer->intensity=pClound->intensity/255.f;
		pClound++;pPointBuffer++;
	}
	ofstream fbin(binPath,ios::out| ios::binary);
    fbin.write( (const char*)(pPointBufferStart),pointsNumber*16);
	free(pPointBufferStart);
	pPointBuffer=nullptr;
    pPointBufferStart=nullptr;
	cout << "write point to txt finished!" << endl;
}
void BatchToBin(vector<string>& files){
	for(uint32_t i=0;i<files.size();i++){
		auto indexOfDot = files[i].find_last_of('.'); 
		const string& pcdPath=string("./pcd_sim/")+files[i];
		const string& binPath=string("./pcd_bin/")+files[i].substr(0,indexOfDot)+string(".bin");
		cout<<"binPath:"<<binPath<<endl;
		ReadPCDfile(pcdPath,binPath);
	}         
}

#ifdef _WIN32
void GetAllFiles_win(const string file_path,vector<string>& files){
    long   hFile = 0;
	struct _finddata_t fileinfo;
	string p;
	if ((hFile = _findfirst(p.assign(file_path).append("\\*").c_str(), &fileinfo)) != -1){
		do{
			if ((fileinfo.attrib &  _A_SUBDIR)){
				if (strcmp(fileinfo.name, ".") != 0 && strcmp(fileinfo.name, "..") != 0)
					GetAllFiles_win(p.assign(file_path).append("\\").append(fileinfo.name), files);
			}
			else{
				const string& file_name = p.assign(file_path).append("\\").append(fileinfo.name);
				files.push_back(file_name.substr(file_name.find_last_of("\\")+1,sizeof(file_name)));
			}
		} while (_findnext(hFile, &fileinfo) == 0);
		_findclose(hFile);
	}
}
#else
void GetAllFiles_ubuntu(const string file_path,vector<string>& files){
	struct dirent *ptr;
	DIR  *dir;
	const char* pFilePath=file_path.c_str();
	dir=opendir(pFilePath);
	cout<<"start print filename:"<<endl;
	while((ptr=readdir(dir))!=NULL){
		if(ptr->d_name[0]=='.')
			continue;
		cout<<"ptr->d_name:"<<ptr->d_name<<' '<<typeid(ptr->d_name).name()<<endl;
		files.push_back(ptr->d_name);
	}
	cout<<"files:"<<files.size()<<endl;
	BatchToBin(files);
	closedir(dir);
}
#endif


int main()
{
    vector<string> files;
#ifdef _WIN32
	const string& file_path = "./pcd_sim";
	GetAllFiles_win(file_path, files);
#else
	const string& file_path = "./pcd_sim";
	GetAllFiles_ubuntu(file_path,files);
#endif
	BatchToBin(files);
	return 0;
}
	
	






