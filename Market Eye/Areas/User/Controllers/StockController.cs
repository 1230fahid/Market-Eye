using System.Collections;
using System.Net;
using System.Security.Claims;
using HtmlAgilityPack;
using MarketEye.DataAccess.Data;
using MarketEye.DataAccess.Data.Repository;
using MarketEye.DataAccess.Data.Repository.IRepository;
using MarketEye.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.Elfie.Model;

namespace Market_Eye.Areas.User.Controllers
{
    [Area("User")]
    [Authorize]
    public class StockController : Controller
    {
        private IUnitOfWork _unitOfWork;
        private HtmlWeb _web;
        public StockController(IUnitOfWork unitOfWork)
        {
			_unitOfWork = unitOfWork;
            _web = new HtmlWeb();

		}

        [HttpGet]
        [Route("Stock")]
        public IActionResult Index()
        {
			var claimsIdentity = (ClaimsIdentity)User.Identity; //type-cast to claims identity
			var claim = claimsIdentity.FindFirst(ClaimTypes.NameIdentifier);
			IQueryable<UserStock> queries = this._unitOfWork.UserStock.FindByUser(claim.Value);
            List<StockTrend> stockTrends = new List<StockTrend>();
            foreach(var query in queries) 
            {
                StockData? stockData = this._unitOfWork.StockData.FindById(query.StockId);
				var url = "https://finviz.com/quote.ashx?t=" + stockData.Symbol + "&ty=c&p=d&b=1";
				var doc = _web.Load(url);
				var currentPrice = doc.DocumentNode.SelectNodes("/html/body/div[2]/div[2]/div[4]/table/tr/td/div/table[1]/tr/td/div[2]/table/tr[11]/td[12]/b");

                StockTrend stockTrend = new StockTrend();
                stockTrend.StockData = stockData;
                stockTrend.CurrentPrice = currentPrice[0].InnerText;
                stockTrends.Add(stockTrend);
			}

			return View(stockTrends);
		}

        [HttpPost]
		[Route("Stock/Add")]
		public IActionResult Add(string symbol)
        {
            var user = User.Identity;
            Console.WriteLine($"user is {user}");
            Console.WriteLine($"symbol is {symbol}");
            var url = "https://finviz.com/quote.ashx?t=" + symbol + "&ty=c&p=d&b=1"; 
			var web = new HtmlWeb();
			var doc = web.Load(url);

            var currentPrice = doc.DocumentNode.SelectNodes("/html/body/div[2]/div[2]/div[4]/table/tr/td/div/table[1]/tr/td/div[2]/table/tr[11]/td[12]/b");
            /*
             * While current price == null, return comment back to user under their stock symbol, saying stock does not exist and prompt them to answer again
             * Else if current price != null, check if stock exists in dbo.StockData based on name
             *      If it does exist then just use it
             *      Else compute weights and add it
             */
            
            if (currentPrice == null) 
            {
                return BadRequest("Error stock not found!");
            }

            string upperSymbol = symbol.ToUpper();
			StockData? data = this._unitOfWork.StockData.FirstOrDefault(upperSymbol);

            /*
             * if (data == null) {
             *     Here we need to do our process
             *     Run optimizer with stock symbol
             *     Predict stock with model
             *     Then add it to database
             * }
             */

			var claimsIdentity = (ClaimsIdentity)User.Identity; //type-cast to claims identity
			var claim = claimsIdentity.FindFirst(ClaimTypes.NameIdentifier);

            UserStock? userStock = this._unitOfWork.UserStock.FirstOrDefault(claim.Value, data.Id);
			if (userStock != null)
			{
				return BadRequest("Stock is already added!");
			}

			Console.WriteLine("currentPrice is ", currentPrice[0].InnerText);
            return Ok("Stock found!");
		}
    }
}
