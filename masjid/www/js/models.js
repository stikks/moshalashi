var app = angular.module('masjid.models');
	
app.factory('User', ['$resource', 'CONSTANT', function($resource, CONSTANT){
	return $resource(CONSTANT.API_URL + '/users/:id', {id: '@id'})
}]);

app.factory('Mosque', ['$resource', 'CONSTANT', function($resource, CONSTANT){
	return $resource(CONSTANT.API_URL + '/mosques/:id', {id: '@id'})
}]);
app.factory('Login', ['$resource', 'CONSTANT', function($resource, CONSTANT){
	return $resource(CONSTANT.API_URL + '/login')
}]);
app.factory('Signup', ['$resource', 'CONSTANT', function($resource, CONSTANT){
	return $resource(CONSTANT.API_URL + '/signup')
}]);
app.factory('Map', ['$resource', 'CONSTANT', function($resource, CONSTANT){
	return $resource(CONSTANT.API_URL + '/maps')
}])
app.factory('HadithList', ['$resource', 'CONSTANT', function($resource, CONSTANT){
	return $resource(CONSTANT.API_URL + '/hadiths')
}])
app.factory('Hadith', ['$resource', 'CONSTANT', function($resource, CONSTANT){
	return $resource(CONSTANT.API_URL + '/hadiths/:id', {id: '@id'})
}])
app.factory('Dua', ['$resource', 'CONSTANT', function($resource, CONSTANT){
	return $resource(CONSTANT.API_URL + '/duas/:id', {id: '@id'})
}])
// 	.factory('ResourceLoader', ['$q', '$stateParams', function($q, $stateParams){

// 	return function(Resource, params) {
//         var delay = $q.defer()

//         Resource.get(params, function(resource) {
//             delay.resolve(resource)
//         }, function() {
//             delay.reject('Unable to fetch data')
//         })

//         return delay.promise
//     }

// }])