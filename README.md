# Strange years

Here we parse and analyse the french “Deceased persons file” from the
[INSEE](https://www.insee.fr) database. We recover thoses datasets using
the api of the [data.gouv.fr](https://www.data.gouv.fr) website.

## Brief overview of the dataset

The Data contains the following entries:

- Family name
- Name
- Gender
- Date of birth
- Code of the locality of birth
- Name of the locality of birth
- Country of birth
- Date of death
- Code of the locality of birth
- Code of the death certificate

With the years of births and deaths, we can graphs the distributions
through time as shown in the figs. 1-3. We can see the impact of the two
world wars in numbers of births during the periods 1915-1919 and
1940-1945.

<figure id="fig:dist">
<img src="figures/year_dist.svg"
alt="Figure 1: Distribution of the years of birth and death in the dataset" />
<figcaption aria-hidden="true">Figure 1: Distribution of the years of
birth and death in the dataset</figcaption>
</figure>

<figure id="fig:M_dist">
<img src="figures/M_year_dist.svg"
alt="Figure 2: Distribution of the years of birth and death for the male" />
<figcaption aria-hidden="true">Figure 2: Distribution of the years of
birth and death for the male</figcaption>
</figure>

<figure id="fig:F_dist">
<img src="figures/F_year_dist.svg"
alt="Figure 3: Distribution of the years of birth and death for the female" />
<figcaption aria-hidden="true">Figure 3: Distribution of the years of
birth and death for the female</figcaption>
</figure>

<figure id="fig:2D_dist">
<img src="figures/year_dist_2D.svg"
alt="Figure 4: Distributions of year of death given the year of birth" />
<figcaption aria-hidden="true">Figure 4: Distributions of year of death
given the year of birth</figcaption>
</figure>

<figure id="fig:M_2D_dist">
<img src="figures/M_year_dist_2D.svg"
alt="Figure 5: Distributions of year of death given the year of birth for the male" />
<figcaption aria-hidden="true">Figure 5: Distributions of year of death
given the year of birth for the male</figcaption>
</figure>

<figure id="fig:F_2D_dist">
<img src="figures/F_year_dist_2D.svg"
alt="Figure 6: Distributions of year of death given the year of birth for the female" />
<figcaption aria-hidden="true">Figure 6: Distributions of year of death
given the year of birth for the female</figcaption>
</figure>
