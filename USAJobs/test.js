var request = require('request');    
const FileSystem = require('fs');
var key = require('./apikey').authKey;
            
var host = 'data.usajobs.gov';  
var userAgent = 'johnso154@students.rowan.edu';  
var authKey = key.authKey;  //note: api not uploaded to github
            
request({      
    url: 'https://data.usajobs.gov/api/search?JobCategoryCode=2210&Keyword=Software Development&LocationName=Philadelphia, PA',      
    method: 'GET',      
    headers: {          
        "Host": host,          
        "User-Agent": userAgent,          
        "Authorization-Key": authKey      
    }  
}, function(error, response, body) {      
    FileSystem.writeFile('USAJobs/output.json', body, (err) => {
        if (err) throw err;
    });
});