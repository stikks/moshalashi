'use strict';
var app = angular.module('masjid.controllers');

app.controller('HomeCtrl', function($scope, localStorageService, Dua, Hadith) {
  
	$scope.dua = new Dua()

	$scope.hadith = new Hadith()

	$scope.$on('$ionicView.enter', function() {

		$scope.dua.$get(function(response){
			$scope.duas = response.query
		})

		$scope.hadith.$get(function(response){
			$scope.hadiths = response.query
		})
	})

})