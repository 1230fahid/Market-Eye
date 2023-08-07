using System.Configuration;
using Reddit;
using RestSharp;
using Reddit.Models.Internal;
using System.Diagnostics;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using MarketEye.Utility;
using MarketEye.DataAccess.Data;
using MarketEye.DataAccess.Data.Repository.IRepository;
using MarketEye.DataAccess.Data.Repository;

var reddit = new RedditClient(appId: "EVmKnLlQ8BUIJriRiemHpw", appSecret: "duW1EV_49oA2YdQw1e1Xq2tthwPIhg", refreshToken: "563986035943-P0Vos3WT70oTDxy60XqaQv6jfPIehw");
var builder = WebApplication.CreateBuilder(args);
var connectionString = builder.Configuration.GetConnectionString("Market_EyeContextConnection") ?? throw new InvalidOperationException("Connection string 'Market_EyeContextConnection' not found.");

builder.Services.AddDbContext<MarketEyeDbContext>(options => options.UseSqlServer(connectionString));
builder.Services.AddDefaultIdentity<Market_EyeUser>().AddEntityFrameworkStores<MarketEyeDbContext>();

builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();

// Add services to the container.
builder.Services.AddControllersWithViews();
//Add razor pages
builder.Services.AddRazorPages();

builder.Services.Configure<IdentityOptions>(options =>
{
    //Password settings
    options.Password.RequireDigit = true;
    options.Password.RequireLowercase = true;
    options.Password.RequireNonAlphanumeric = true;
    options.Password.RequireUppercase = true;
    options.Password.RequiredLength = 6;

    //Lockout settings
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(5);
    options.Lockout.MaxFailedAccessAttempts = 5;
    options.Lockout.AllowedForNewUsers = true;

    //User settings
    options.User.AllowedUserNameCharacters =
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._@+";
    options.User.RequireUniqueEmail = false;
});

builder.Services.ConfigureApplicationCookie(options =>
{
    // Cookie settings
    options.Cookie.HttpOnly = true;
    options.ExpireTimeSpan = TimeSpan.FromHours(6);

    options.LoginPath = "/Login";
    options.LogoutPath = "/Logout";
    options.AccessDeniedPath = "/AccessDenied";
    options.SlidingExpiration = true;
});

builder.Services.AddSingleton(reddit);


var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthentication(); //enables Identity
app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{area=User}/{controller=Home}/{action=Index}/{id?}");

app.MapRazorPages();
app.Run();
