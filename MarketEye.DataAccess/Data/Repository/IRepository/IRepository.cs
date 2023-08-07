using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using MarketEye.Models;

namespace MarketEye.DataAccess.Data.Repository.IRepository
{
	public interface IRepository<T>
	{
		public void Add(T obj);
	}
}
