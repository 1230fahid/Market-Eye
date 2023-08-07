using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MarketEye.DataAccess.Data.Repository.IRepository;
using MarketEye.Models;
using Microsoft.EntityFrameworkCore;

namespace MarketEye.DataAccess.Data.Repository
{
	public class Repository<T> : IRepository<T> where T : class
	{
		private MarketEyeDbContext _dbContext;
		internal DbSet<T> dbSet;
		public Repository(MarketEyeDbContext dbContext) 
		{ 
			this._dbContext = dbContext;
			this.dbSet = this._dbContext.Set<T>();
		}
		public void Add(T obj)
		{
			this.dbSet.Add(obj);
		}
	}
}
