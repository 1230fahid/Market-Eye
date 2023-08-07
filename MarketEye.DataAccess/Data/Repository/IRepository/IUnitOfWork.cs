using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MarketEye.DataAccess.Data.Repository.IRepository
{
	public interface IUnitOfWork
	{
		public IUserStockRepository UserStock { get; }
		public IStockDataRepository StockData { get; }
		public int SaveChanges();
	}
}
