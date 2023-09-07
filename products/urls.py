from django.urls import path
from .views import(

  ProductList, # MD, DT, Chairman, # Chairman, MD, DT, Done
  market_agents_products_all, # Chairman, MD, DT Done
  admin_market_agent_products,

  ProductCreate, # DT, Done
  ProductUpdate, # DT, Done
  delete_picture, # DT, Done
  delete_specification, # DT, Done
  product_details_admin,  # MD, DT, Chairman
  ProductDeleteView,# DT

  market_agent_product_create,
  market_agent_products_list,
  market_agent_product_edit,
  market_agent_product_details, # Agent
  MarketAgentProductDeleteView, # Agent
   
  public_products, # Done
  public_product_details, # Done
  # get_location_data,

  get_excel_file
)

app_name  = 'products'


urlpatterns = [
    
    path('', public_products, name = 'public-products'), # Public
    # path('location/', get_location_data, name = 'location'), # Public
    path('add/', ProductCreate.as_view(), name='product-create'), # Director Technical
    path('agents/products/all/', market_agents_products_all, name='market-agent-products-all'), # Director Technical, MD, Chairman
    path('agent/product/add/', market_agent_product_create, name='market-agent-product-create'),
    
    path('agent/<str:agent>/products/', admin_market_agent_products, name='admin-market-agent-products'),

    path('agent/products/', market_agent_products_list, name='market-agent-products-list'),
        
    path('csv-file/', get_excel_file, name='get-file'), # Director Technical, MD, Chairman
    path('list/all/', ProductList.as_view(), name='products-list-all'), # and Director Technical

    path('<int:id>/', public_product_details, name = 'public-product-details'), #public

    path('<int:pk>/pic/delete/', delete_picture, name='delete-picture'), # Director Technical
    path('<int:pk>/spec/delete/', delete_specification, name='delete-specification'), # Director Technical
    path('<slug:category_slug>/', public_products, name='public_product_list_by_category'),
    path('<int:pk>/prod/update/', ProductUpdate.as_view(), name='product-update'), # Director Technical
    path('<int:id>/admin/prod/', product_details_admin, name='product-details-admin'),
    path('<int:id>/a/product/edit/', market_agent_product_edit, name='market-agent-product-edit'),
    path('<int:id>/a/product/', market_agent_product_details, name='market-agent-product-details'),
    path('<int:pk>/a/product/delete/', MarketAgentProductDeleteView.as_view(), name='market-product-delete'),
    path('<int:pk>/prod/delete/', ProductDeleteView.as_view(), name='product-delete-admin'),
    
]