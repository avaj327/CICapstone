var request = require('request');    
const FileSystem = require('fs');
            
var host = 'data.usajobs.gov';  
var userAgent = 'johnso154@students.rowan.edu';  
var authKey = 'EEF47C5F-7E2E-4201-A2C9-F6787A7278E1';    
            
request({      
    url: 'https://data.usajobs.gov/api/search?JobCategoryCode=2210&Keyword=Software Development&LocationName=Philadelphia, PA',      
    method: 'GET',      
    headers: {          
        "Host": host,          
        "User-Agent": userAgent,          
        "Authorization-Key": authKey      
    }  
}, function(error, response, body) {      
    FileSystem.writeFile('output.json', body, (err) => {
        if (err) throw err;
    });
});