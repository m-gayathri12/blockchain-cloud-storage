pragma solidity >= 0.8.11 <= 0.8.11;
pragma experimental ABIEncoderV2;
//Deduplicate solidity code
contract Deduplicate {

    uint public userCount = 0; 
    mapping(uint => user) public userList; 
     struct user
     {
       string username;
       string password;
       string phone;
       string email;
       string home_address;
     }
 
   // events 
   event userCreated(uint indexed _userId);
   
   //function  to save user details to Blockchain
   function saveUser(string memory uname, string memory pass, string memory phone, string memory em, string memory add) public {
      userList[userCount] = user(uname, pass, phone, em, add);
      emit userCreated(userCount);
      userCount++;
    }

     //get user count
    function getUserCount()  public view returns (uint) {
          return  userCount;
    }

    uint public metadataCount = 0; 
    mapping(uint => metadata) metadataList; 
     struct metadata
     {
       string username;
       string filename;
       string block_no;
       string block_hash;
       string upload_date;              
     }
 
   // events 
   event metadataCreated(uint indexed _metadataId);
   
   //function  to save metadata details to Blockchain
   function saveMetadata(string memory uname, string memory fname, string memory bno, string memory bhash, string memory ud) public {
      metadataList[metadataCount] = metadata(uname, fname, bno, bhash, ud);
      emit metadataCreated(metadataCount);
      metadataCount++;
    }

    //get metadata count
    function getMetadataCount()  public view returns (uint) {
          return metadataCount;
    }

    function getUsername(uint i) public view returns (string memory) {
        user memory doc = userList[i];
	return doc.username;
    }

    function getPassword(uint i) public view returns (string memory) {
        user memory doc = userList[i];
	return doc.password;
    }

    function getPhone(uint i) public view returns (string memory) {
        user memory doc = userList[i];
	return doc.phone;
    }    

    function getEmail(uint i) public view returns (string memory) {
        user memory doc = userList[i];
	return doc.email;
    }

    function getAddress(uint i) public view returns (string memory) {
        user memory doc = userList[i];
	return doc.home_address;
    }

    function getOwner(uint i) public view returns (string memory) {
        metadata memory doc = metadataList[i];
	return doc.username;
    }

    function getFilename(uint i) public view returns (string memory) {
        metadata memory doc = metadataList[i];
	return doc.filename;
    }

    function getBlockhash(uint i) public view returns (string memory) {
        metadata memory doc = metadataList[i];
	return doc.block_hash;
    }   
    
    function getBlockNo(uint i) public view returns (string memory) {
        metadata memory doc = metadataList[i];
	return doc.block_no;
    } 

     function getUploadDate(uint i) public view returns (string memory) {
        metadata memory doc = metadataList[i];
	return doc.upload_date;
    } 
     
}