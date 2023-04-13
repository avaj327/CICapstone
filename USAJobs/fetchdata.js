var request = require('request');    
const FileSystem = require('fs');
            
var host = 'data.usajobs.gov';  
var userAgent = 'johnso154@students.rowan.edu';  
var authKey = require('./apikey').authKey;  //note: api not uploaded to github
            

function find_and_trim(location) {
	//find
	request({      
		url: 'https://data.usajobs.gov/api/search?JobCategoryCode=2210&Keyword=Software Development&LocationName=' + location,      
		method: 'GET',      
		headers: {          
			"Host": host,          
			"User-Agent": userAgent,          
			"Authorization-Key": authKey      
		}  
	}, function(error, response, body) {     

		//trim
		let jsonArray = JSON.parse(body);
		jsonArray = jsonArray.SearchResult.SearchResultItems;

		let trimmedArray = []
		jsonArray.forEach(element => {
			trimmedArray.push(element.MatchedObjectDescriptor);
		});

		//restructure
		let restructuredArray = []
		trimmedArray.forEach(element => {
			let a = {};

			a.DepartmentName = element.DepartmentName;
			a.PositionTitle = element.PositionTitle;
			a.PositionURI = element.PositionURI;
			
			//only include location if there is an opening in area searched for
			element.PositionLocation.forEach(loc => {
				if (loc.LocationName == location) {
					a.PositionLocation = loc.LocationName;
				}
			});

			a.JobDuties = element.UserArea.Details.MajorDuties;
			
			//only push to array if the location is correct -- the search params should ensure this, but just to double check
			if (a.PositionLocation == location) {
				restructuredArray.push(a);
			}			
		}); //end restructure

		const city = location.split(",")[0];
		FileSystem.writeFile('USAJobs/data/' + city + '_output.json', JSON.stringify(restructuredArray), (err) => {
			if (err) throw err;
		});
		
	}); //end request function	


} //end find_and_trim


//EAST
find_and_trim("Washington, District of Columbia");
find_and_trim("New York, New York");
find_and_trim("Philadelphia, Pennsylvania");

//NORTH
find_and_trim("Detroit, Michigan");
find_and_trim("Billings, Montana");
find_and_trim("Minneapolis, Minnesota");

//WEST
find_and_trim("Los Angeles, California");
find_and_trim("Portland, Oregon");
find_and_trim("Seattle, Washington");

//SOUTH
find_and_trim("Phoenix, Arizona");
find_and_trim("Houston, Texas");
find_and_trim("Atlanta, Georgia");