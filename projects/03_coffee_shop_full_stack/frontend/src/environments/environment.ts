export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'udacity-segel.eu', // the auth0 domain prefix
    audience: 'https://coffe-shop-api.segelmark.com', // the audience set for the auth0 app
    clientId: 'UFS1f21f11r1YF6FJmPa2L1P08Te8wy3', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
