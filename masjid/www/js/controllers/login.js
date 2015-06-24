'use strict';
var app = angular.module('masjid.controllers');

app.controller('LoginController', function($scope, Login){
	
	$scope.errors = {}

	$scope.obj = new Login()

	$scope.doLogin = function() {

		$scope.obj.$save(function(response){
			$scope.setUser(response.user)
			$scope.closeLogin()
		},
		function(error){
			if(error.status==34){
				$scope.errors = error.data
			}
		})
	}

})

app.controller('SignupCtrl', function($scope, Signup){
	
})