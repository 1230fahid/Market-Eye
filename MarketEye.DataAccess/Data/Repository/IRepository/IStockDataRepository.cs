using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MarketEye.Models;

namespace MarketEye.DataAccess.Data.Repository.IRepository
{
	public interface IStockDataRepository
	{
		public StockData? FirstOrDefault(string symbol);
		public StockData? FindById(int stockId);
		public void Add(StockData stockData);
	}
}
