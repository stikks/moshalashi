var app = angular.module('masjid.controllers');

app.controller('MosqueCtrl', function($scope, localStorageService, Map){

  	$scope.getPosition()

  	var position = localStorageService.get('position')

  	$scope.map =  new Map()

	$scope.map.latitude = position.latitude

	$scope.map.longitude = position.longitude

	$scope.map.$save(function(response){
	  	$scope.mosques = response.result
	},
	function(error){
	  console.log(error)
	})

})

app.controller('MapCtrl', function($scope){
	$scope.$on('$ionicView.enter', function(){
		$scope.getPosition()
		$scope.loadMosques()
		// $scope.drawMap();
	})
})