using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MarketEye.DataAccess.Data.Repository.IRepository;
using MarketEye.Models;

namespace MarketEye.DataAccess.Data.Repository
{
	public class UserStockRepository : Repository<UserStock>, IUserStockRepository
	{
		private MarketEyeDbContext _dbContext;
		public UserStockRepository(MarketEyeDbContext dbContext) : base(dbContext)
		{
			this._dbContext = dbContext;
		}

		public UserStock? FirstOrDefault(string userId, int stockId)
		{
			return this._dbContext.UserStocks.FirstOrDefault(s => s.UserId == userId && s.StockId == stockId);
		}

		public IQueryable<UserStock> FindByUser(string userId)
		{
			return this._dbContext.UserStocks.Where(s => s.UserId == userId);
		}
	}
}
