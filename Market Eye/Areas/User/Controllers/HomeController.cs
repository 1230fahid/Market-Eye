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