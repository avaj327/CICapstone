const mongoose = require('mongoose'); //mongodb interface
const connectionString = require('./apikey').databaseURL;
const FileSystem = require('fs');

async function connect() {

	await mongoose.connect(connectionString, {})
		.then(db => console.log('Connected with MongoDB.'))
		.catch(err => console.log(`Unable to connect with MongoDB: ${err.message}`));


	const entrySchema = mongoose.Schema({
		Department_Name: String,
		Position_Title: String,
		Position_URI: String,
		Position_Location: String,
		Job_Duties: [String]

	});

	var dataFolder = await FileSystem.promises.readdir("./USAJobs/data");

	const Model = mongoose.model("jobs_data", entrySchema, 'jobs_data');
	await Model.collection.drop();

	for (const file of dataFolder) {
		const jsonArray = require('./data/' + file);
		await Model.insertMany(jsonArray);
	}



	mongoose.connection.close();
}

connect();