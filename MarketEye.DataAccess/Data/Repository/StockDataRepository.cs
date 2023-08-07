using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MarketEye.DataAccess.Data.Repository.IRepository;
using MarketEye.Models;

namespace MarketEye.DataAccess.Data.Repository
{
	public class StockDataRepository : Repository<StockData>, IStockDataRepository
	{
		private MarketEyeDbContext _dbContext;
		public StockDataRepository(MarketEyeDbContext dbContext) : base(dbContext)
		{
			this._dbContext = dbContext;
		}

		public StockData? FirstOrDefault(string symbol)
		{
			return this._dbContext.StockDatas.FirstOrDefault(s => s.Symbol == symbol);
		}

		public StockData? FindById(int stockId)
		{
			return this._dbContext.StockDatas.FirstOrDefault(s => s.Id == stockId);
		}
	}
}
