using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MarketEye.Models;
using Microsoft.EntityFrameworkCore;

namespace MarketEye.DataAccess.Data
{
	public interface IDbContext
	{
		public DbSet<UserStock> UserStocks { get; set; }
		public DbSet<StockData> StockDatas { get; set; }

		public int SaveChanges();
	}
}
