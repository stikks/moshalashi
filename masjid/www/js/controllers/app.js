angular.module('masjid.controllers', ['ngCordova', 'LocalStorageModule'])

.controller('AppCtrl', function($scope, $rootScope, $ionicModal, $timeout, $cordovaOauth, $cordovaDevice, $cordovaGeolocation, localStorageService, Map, $state, $ionicSlideBoxDelegate, $cordovaSocialSharing, CONSTANT, $http, $ionicPlatform) {
  
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  // Create the login modal that we will use later
  $scope.prepareLoginModal = function() {
    $ionicModal.fromTemplateUrl('templates/login.html', {
      scope: $scope,
      animation: 'slide-in-up'
    }).then(function(modal) {
      $scope.modal = modal;
    });
  }
  // Triggered in the login modal to close it
  $scope.closeLogin = function() {
    $scope.modal.hide();
  };

  $scope.prepareSignupModal = function() {
    $ionicModal.fromTemplateUrl('templates/signup.html', {
      scope: $scope,
      animation: 'slide-in-up'
    }).then(function(modal) {
      $scope.SignupModal = modal;
    });

    $scope.$on('$destroy', function() {
      $scope.modal.remove();
    });
  }

  $scope.closeSignupModal = function() {
    $scope.SignupModal.hide();
  }

  $scope.reload = function(){
    $state.go($state.current, {}, {reload: true});
  }

  $scope.changePage = function(index) {
    $state.go(index)
  }

  $scope.slider = function(index){
    $ionicSlideBoxDelegate.slide(index, 500);
  }

  $scope.next = function() {
    $ionicSlideBoxDelegate.next();
  }

  $scope.previous = function() {
    $ionicSlideBoxDelegate.previous();
  }

  // Open the login modal
  $scope.login = function() {
    $scope.modal.show();
  };

  $scope.setUser = function(user){
    $rootScope.user = user
    localStorageService.set('user', user)
  }

  $scope.isLoggedIn = function(){
    var user = localStorageService.get('user')
    if(user){
      return true
    }
    else{
      return false
    }
  }

  $scope.logout = function(){
    $scope.user = {}
    localStorageService.remove('user')
  }

  $scope.position = {}

  // $scope.isWebView = ionic.Platform.isWebView();
  // $scope.isIPad = ionic.Platform.isIPad();
  // $scope.isIOS = ionic.Platform.isIOS();
  // $scope.isAndroid = ionic.Platform.isAndroid();
  // $scope.isWindowsPhone = ionic.Platform.isWindowsPhone();


  $scope.getPosition = function() {

    var posOptions = {timeout: 10000, enableHighAccuracy: false};

    $cordovaGeolocation.getCurrentPosition(posOptions).then(function(position){

      localStorageService.set('position', position.coords)

    }, function(error){
      console.log(error)
    })
  };

  $scope.getAddress = function(LatLng) {

    $http.get(CONSTANT.GEOCODE_URL+ LatLng + '&location_type=ROOFTOP&result_type=street_address' + '&key=' + CONSTANT.API_KEY).success(function(response){
      localStorageService.set('currentLocation', response.formatted_address)
    }).error(function(error){
      console.log(error)
    })

  }


  $scope.loadMosques = function() {

    function initialize() {

      var position = localStorageService.get('position')

      var search = new google.maps.LatLng(position.latitude, position.longitude)

      map = new google.maps.Map(document.getElementById('map'), {
        center: search,
        zoom: 15
      });

      var request = {
        location: search,
        // radius: 5000,
        types: ['mosque'],
        rankBy: google.maps.places.RankBy.DISTANCE
      }

      $scope.infowindow = new google.maps.InfoWindow();
      var service = new google.maps.places.PlacesService(map)
      service.nearbySearch(request, callback)

      $scope.map = map
    }

    function callback(results, status) {
      if (status == google.maps.places.PlacesServiceStatus.OK) {
        for (var i = 0; i < results.length; i++) {
          createMarker(results[i]);
        }
      }
    }

    function createMarker(place) {
      var placeLoc = place.geometry.location;
      var marker = new google.maps.Marker({
        map: $scope.map,
        position: place.geometry.location
      });

      google.maps.event.addListener(marker, 'click', function() {
        $scope.infowindow.setContent(place.name);
        $scope.infowindow.open($scope.map, this);
      });
    }

    google.maps.event.addDomListener(window, 'load', initialize);
    initialize();
  }

  $scope.prepareShareModal = function() {
    $ionicModal.fromTemplateUrl('templates/share.html', {
          scope: $scope,
          animation: 'slide-in-up'
      }).then(function(modal) {
          $scope.shareModal = modal
      })

      $scope.$on('$destroy', function() {
          $scope.shareModal.remove();
      })
  }


  $scope.prepareAboutModal = function() {
    $ionicModal.fromTemplateUrl('templates/about.html', {
          scope: $scope,
          animation: 'slide-in-up'
      }).then(function(modal) {
          $scope.aboutModal = modal
      })

      $scope.$on('$destroy', function() {
          $scope.aboutModal.remove();
      })
  }


  $scope.openShareModal = function() {
    $scope.shareModal.show();
  }

  $scope.shareApp = function(type, msg) {

    document.addEventListener("deviceready", function () {

      console.log('type')

      $scope.device = $cordovaDevice.getDevice();

      if(msg ==  null) {  
        var message = CONSTANT.SHARE_MESSAGE + $scope.device.platform
      }
      else {
        var message = msg
      }

      var link = ''

      if($scope.device.platform == 'Android'){
        link = CONSTANT.GOOGLE_PLAY_URL
      }
      else{
        link = CONSTANT.IOS_URL
      }

      $cordovaSocialSharing.canShareVia(type, message, null, link).then(function(response) {
          console.log(response)
          $scope.shareModal.hide()
        }, function(err) {
          console.log(error)
          $scope.shareModal.hide()
      });

    }, false);
      
  }

  $scope.basicShare = function() {

    console.log('here')

    document.addEventListener("deviceready", function () {

      console.log('really here')

      $scope.device = $cordovaDevice.getDevice();

      var message = CONSTANT.SHARE_MESSAGE + $scope.device.platform

      $cordovaSocialSharing
      .share(message, null, null, 'http://link') // Share via native share sheet
      .then(function(response) {
        console.log(response)
        $scope.shareModal.hide()
      }, function(error) {
        console.log(error)
        $scope.shareModal.hide()
      })
    })
  }


  $scope.checkIn = function() {

    $scope.getPosition()
    $scope.getAddress()
    $scope.openShareModal()

  }

  $scope.facebookLogin = function() {
    $cordovaOauth.facebook(CONSTANT.FACEBOOK_CLIENT_ID, ["scorpiodem@yahoo.com"]).then(function(result) {
        // results
        console.log(result)
    }, function(error) {
        // error
    });
  }

  $scope.googleLogin = function() {
    $cordovaOauth.google(CONSTANT.GOOGLE_CLIENT_ID, ["https://www.googleapis.com/auth/urlshortener", "https://www.googleapis.com/auth/userinfo.email"]).then(function(result) {
        console.log(JSON.stringify(result));
    }, function(error) {
        console.log(error);
    });
  }

  $scope.slider = function(index){
    $ionicSlideBoxDelegate.slide(index, 500);
  }

  $scope.next = function() {
    $ionicSlideBoxDelegate.next();
  }

  $scope.previous = function() {
    $ionicSlideBoxDelegate.previous();
  }

  $scope.prepareLoginModal()
  $scope.prepareSignupModal()
  $scope.prepareShareModal()
  $scope.prepareAboutModal()

})
