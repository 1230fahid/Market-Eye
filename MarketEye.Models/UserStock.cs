using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using MarketEye.Utility;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc.ModelBinding.Validation;

namespace MarketEye.Models
{
    public class UserStock
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public string UserId { get; set; }
        [ForeignKey("UserId")]
        [ValidateNever]
        public Market_EyeUser Market_EyeUser { get; set; }

        [Required]
        public int StockId { get; set; }
        [ForeignKey("StockId")]
        [ValidateNever]
        public StockData StockData { get; set; }

    }
}