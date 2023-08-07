using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using MarketEye.Models;
using MarketEye.Utility;

namespace MarketEye.DataAccess.Data
{
	public class MarketEyeDbContext: IdentityDbContext<Market_EyeUser>, IDbContext
    {
		public MarketEyeDbContext(DbContextOptions<MarketEyeDbContext> options):base(options) { }
		public DbSet<UserStock> UserStocks { get; set; }
		public DbSet<StockData> StockDatas { get; set; }

		public override int SaveChanges()
		{
			return this.SaveChanges();
		}
	}

}
