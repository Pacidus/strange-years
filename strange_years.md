# Strange years
Here we parse and analyse the french "Deceased persons file" from the [INSEE](https://www.insee.fr) database.
We recover thoses datasets using the api of the [data.gouv.fr](https://www.data.gouv.fr) website.

## Brief overview of the dataset

The Data contains the following entries:

* Family name
* Name
* Gender 
* Date of birth
* Code of the locality of birth
* Name of the locality of birth
* Country of birth
* Date of death
* Code of the locality of birth
* Code of the death certificate

With the years of births and deaths, we can graphs the distributions through
time as shown in the [@fig:dist; @fig:M_dist; @fig:F_dist].
We can see the impact of the two world wars in numbers of births during the periods 1915-1919 and 1940-1945. 

![Distribution of the years of birth and death in the dataset](figures/year_dist.svg){#fig:dist}

![Distribution of the years of birth and death for the male](figures/M_year_dist.svg){#fig:M_dist}

![Distribution of the years of birth and death for the female](figures/F_year_dist.svg){#fig:F_dist}


![Distributions of year of death given the year of birth](figures/year_dist_2D.svg){#fig:2D_dist}

![Distributions of year of death given the year of birth for the male](figures/M_year_dist_2D.svg){#fig:M_2D_dist}

![Distributions of year of death given the year of birth for the female](figures/F_year_dist_2D.svg){#fig:F_2D_dist}

