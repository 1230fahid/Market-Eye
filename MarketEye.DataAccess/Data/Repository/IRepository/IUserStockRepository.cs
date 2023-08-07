using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MarketEye.Models;

namespace MarketEye.DataAccess.Data.Repository.IRepository
{
	public interface IUserStockRepository
	{
		public UserStock? FirstOrDefault(string userId, int stockId);
		public IQueryable<UserStock> FindByUser(string userId);
		public void Add(UserStock userStock);
	}
}
