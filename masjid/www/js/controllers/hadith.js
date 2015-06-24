'use strict';
var app = angular.module('masjid.controllers');


app.controller('HadithListCtrl', function($scope, $rootScope, HadithList, $ionicModal, Hadith, localStorageService){
	
	$scope.hadith = new HadithList()

	$scope.hadith.$get(function(response){
		$scope.hadiths = response.query
	},
	function(error){
		console.log(error)
	})

	$ionicModal.fromTemplateUrl('add_hadith.html', {
	    scope: $scope,
	    animation: 'slide-in-up'
	}).then(function(modal) {
	    $scope.modal = modal;
	});

	$scope.addHadith = function() {
    	$scope.modal.show()
  	}

  	$scope.closeModal = function() {
    	$scope.modal.hide();
  	}

	$scope.$on('$destroy', function() {
		$scope.modal.remove();
	});

	$scope.save = function() {

		var user = localStorageService.get('user')

		if(user){
			$scope.hadith.user_id = user.id
		}

		$scope.hadith.$save(function(response){
			$scope.closeModal()
			$scope.reload()
		},
		function(error){
			console.log(error)
		})
	}

})