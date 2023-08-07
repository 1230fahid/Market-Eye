using Market_Eye.Models;
using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using Reddit;
using System.Net;
using Microsoft.AspNetCore.Identity;
using RestSharp.Authenticators;
using RestSharp;

namespace Market_Eye.Controllers
{
    [Area("User")]
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private RedditClient _reddit;

        public HomeController(RedditClient reddit)
        {
            _reddit = reddit;
        }

        //[JSON].access_token

        public IActionResult Index(String? state = null, String? code = null)
        {
            /*
            if (state != null && code != null)
            {
                //Get refresh token
                String tokenUrl = "https://www.reddit.com/api/v1/access_token";
                var options = new RestClientOptions(tokenUrl)
                {

                    Authenticator = new HttpBasicAuthenticator("EVmKnLlQ8BUIJriRiemHpw", "duW1EV_49oA2YdQw1e1Xq2tthwPIhg"),
                    UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                };

                RestSharp.RestClient rc = new RestClient(options);
                RestSharp.RestRequest token = new RestSharp.RestRequest(tokenUrl, RestSharp.Method.Post);
                token.AddParameter("grant_type", "authorization_code");
                token.AddParameter("code", code); //random value
                token.AddParameter("redirect_uri", "https://localhost:44387/");
                token.RequestFormat = RestSharp.DataFormat.Json;

                RestSharp.RestResponse tokenResponse = (RestSharp.RestResponse)rc.Execute(token);
                RestSharp.ResponseStatus tokenResponseStatus = tokenResponse.ResponseStatus;
            }
            */


            // Display the name and cake day of the authenticated user.
            /*Console.WriteLine("_reddit is " + _reddit);
            Console.WriteLine("Username: " + _reddit.Account.Me.Name);
            Console.WriteLine("Cake Day: " + _reddit.Account.Me.Created.ToString("D"));

            // Get info on another subreddit.
            var subReddit = _reddit.Subreddit("wallstreetbets");
            var askReddit = subReddit.About();

            Console.WriteLine("subReddit.Flairs.LinkFlairV2 is:\n", subReddit.Flairs.LinkFlairV2.ToArray());

            // Get the top post from a subreddit.
            var topPost = askReddit.Posts.Top[0];*/


            /*MSFT data
            var client = new RestClient("https://alpha-vantage.p.rapidapi.com/query?interval=5min&function=TIME_SERIES_INTRADAY&symbol=MSFT&datatype=json&output_size=compact");
            var request = new RestRequest(Method.GET);
            request.AddHeader("X-RapidAPI-Key", "2d9682785bmsh125a8783b4d4e57p1db292jsnc2cd9580c1c8");
            request.AddHeader("X-RapidAPI-Host", "alpha-vantage.p.rapidapi.com");
            IRestResponse response = client.Execute(request);
            */

            /*
            var client2 = new RestClient("https://alpha-vantage.p.rapidapi.com/query?symbol=MSFT&function=TIME_SERIES_MONTHLY&datatype=json");
            var request2 = new RestRequest(Method.GET);
            request2.AddHeader("X-RapidAPI-Key", "2d9682785bmsh125a8783b4d4e57p1db292jsnc2cd9580c1c8");
            request2.AddHeader("X-RapidAPI-Host", "alpha-vantage.p.rapidapi.com");
            IRestResponse response2 = client2.Execute(request2);
            */

            return View();
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}