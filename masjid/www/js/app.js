// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'starter.controllers' is found in controllers.js
angular.module('masjid.models', ['ionic', 'ngResource'])
angular.module('masjid.controllers', ['LocalStorageModule'])
var app = angular.module('masjid', ['ionic', 'masjid.controllers', 'masjid.models', 'ngResource', 'LocalStorageModule', 'ngCordovaOauth', 'ngAnimate', 'ngTouch', 'ngCordova'])

app.config(function($stateProvider, $urlRouterProvider, localStorageServiceProvider, $ionicConfigProvider) {

  $ionicConfigProvider.scrolling.jsScrolling(false);
  $ionicConfigProvider.tabs.position('bottom');

  localStorageServiceProvider.setPrefix('masjid');

  $stateProvider

  .state('app', {
    url: "/app",
    abstract: true,
    templateUrl: "templates/menu.html",
    controller: 'AppCtrl'
  })

  .state('app.search', {
    url: "/search",
    views: {
      'menuContent': {
        templateUrl: "templates/search.html"
      }
    }
  })
  .state('app.home', {
    url: "/home",
    views: {
      'menuContent': {
        templateUrl: "templates/home.html",
        controller: 'HomeCtrl'
      }
    }
  })
  .state('app.events', {
    url: '/events',
    views: {
      'menuContent': {
        templateUrl: '/templates/events.html',
        controller: 'EventsCtrl'
      }
    }
  })
  .state('app.mosques',{
    url: '/mosques',
    views: {
      'menuContent': {
        templateUrl: 'templates/mosques.html',
        controller: 'MosqueCtrl'
      }
    }
  })
  .state('app.mosque',{
    url: '/mosques/:id',
    views: {
      'menuContent': {
        templateUrl: 'templates/mosque.html',
        controller: 'MosqueCtrl'
      }
    }
  })
  .state('app.profile', {
    url: "/users/:id",
    views: {
      'menuContent': {
        templateUrl: "templates/profile.html",
        controller: 'ProfileCtrl'
      }
    }
  })
  .state('app.duas', {
    url: 'duas',
    views: {
      'menuContent': {
        templateUrl: 'templates/duas.html',
        controller: 'DuaCtrl'
      }
    }
  })
  .state('app.map', {
    url: 'map',
    views: {
      'menuContent': {
        templateUrl: 'templates/map.html',
        controller: 'MapCtrl'
      }
    }
  })
  .state('app.hadiths', {
    url: 'hadiths',
    views: {
      'menuContent': {
        templateUrl: 'templates/hadith.html',
        controller: 'HadithListCtrl'
      }
    }
  });
  // .state('app.hadith', {
  //   url: "/hadiths",
  //   views: {
  //     'menuContent': {
  //       templateUrl: "templates/hadith.html"
  //     }
  //   }
  // })
  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise('/app/home');
});

app.constant('CONSTANT', {
  'API_URL': 'http://localhost:5000/api/v1',
  'API_KEY': 'AIzaSyC6iPANJCIRU9fUNXMKr5gt3pyKGgOqjiE',
  'SHARE_MESSAGE': "Check out this cool app i'm using called '' for",
  'GOOGLE_PLAY_URL': '',
  'IOS_URL': '',
  'GEOCODE_URL': "https://maps.googleapis.com/maps/api/geocode/json?latlng=",
  'FACEBOOK_CLIENT_ID': '451439515026138',
  'GOOGLE_CLIENT_ID': "866124183575-m43i15mb46h08jqth8dsumrslsau3317.apps.googleusercontent.com"
})


app.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if (window.cordova && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
    }
    if (window.StatusBar) {
      // org.apache.cordova.statusbar required
      StatusBar.styleDefault();
    }
  });
})