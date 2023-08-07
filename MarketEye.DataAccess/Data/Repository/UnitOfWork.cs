using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MarketEye.DataAccess.Data.Repository.IRepository;

namespace MarketEye.DataAccess.Data.Repository
{
	public class UnitOfWork : IUnitOfWork
	{
		private MarketEyeDbContext _dbContext;
		public IUserStockRepository UserStock { get; private set; }
		public IStockDataRepository StockData { get; private set; }
		public UnitOfWork(MarketEyeDbContext dbContext) 
		{ 
			this._dbContext = dbContext;
			this.UserStock = new UserStockRepository(this._dbContext);
			this.StockData = new StockDataRepository(this._dbContext);
		}

		public int SaveChanges()
		{
			return this._dbContext.SaveChanges();
		}
	}
}
