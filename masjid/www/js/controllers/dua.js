'use strict';
var app = angular.module('masjid.controllers');


app.controller('DuaCtrl', function($state, $scope, $ionicModal, Dua, localStorageService){
	
	$scope.dua = new Dua()

	$scope.$on('$ionicView.enter', function() {

        $scope.dua.$get(function(response){
			$scope.objects = response.query
		},
		function(error){
			console.log(error)
		})
	})
		

	$ionicModal.fromTemplateUrl('add_dua.html', {
	    scope: $scope,
	    animation: 'slide-in-up'
	}).then(function(modal) {
	    $scope.modal = modal;
	});

	// $scope.addDua = function() {
 //    	$scope.modal.show()
 //  	}

 //  	$scope.closeModal = function() {
 //    	$scope.modal.hide();
 //  	}

	$scope.$on('$destroy', function() {
		$scope.modal.remove();
	});

	$scope.save = function() {

		var user = localStorageService.get('user')

		$scope.dua.user_id = user.id

		$scope.dua.$save(function(response){
			$scope.modal.hide()
			$state.go('app.duas')
		},
		function(error){
			console.log(error)
		})
	}

})